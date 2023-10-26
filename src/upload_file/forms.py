from django import forms
import gettext

_ = gettext.gettext

def username_is_valid(value):
    if "/" in value:
        raise forms.ValidationError(_('Invalid username. Please remove / substring from the username.'), code='invalid')

class UploadFileForm(forms.Form):
    username = forms.CharField(
                                max_length=50,
                                validators =[username_is_valid]
                            )
    file = forms.FileField(
        label='Select a file'
    )

