# forms.py
from django import forms
from .models import UserProfile

class DocumentForm(forms.ModelForm):
    filename = forms.CharField(max_length=255, label='File Name')
    upload_type = forms.ChoiceField(choices=[('new_folder', 'Create New Folder'), ('existing_folder', 'Choose Existing Folder')], widget=forms.RadioSelect, initial='new_folder')
    folder_name = forms.CharField(max_length=255, required=False, label='New Folder Name')

    class Meta:
        model = UserProfile
        fields = ('document', 'folder_name', 'filename', 'upload_type')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['existing_folders'] = forms.ModelChoiceField(queryset=user.userprofile_set.values_list('folder', flat=True).distinct(), required=False, label='Existing Folders')

    def clean_document(self):
        document = self.cleaned_data['document']
        if document:
            if not document.name.endswith(('.jpg', '.jpeg', '.png', '.pdf')):
                raise forms.ValidationError("Only JPG, PNG, and PDF files are allowed.")
        return document
