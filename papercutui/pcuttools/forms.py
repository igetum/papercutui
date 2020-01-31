from django import forms

class UploadFileForm(forms.Form):
    importfile = forms.FileField()