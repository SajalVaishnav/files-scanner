from django import forms
import gettext

_ = gettext.gettext

def values_are_nums(value):
    for key, value in value.items():
        if(type(value) != int or value < 0):
            raise forms.ValidationError(_('One or more invalid sensitivity score. Please enter only positive numbers as values in the JSON document.'))

class KeyWordsForm(forms.Form):
    keywords = forms.JSONField(
        validators =[values_are_nums]
    )
    
