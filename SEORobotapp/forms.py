from django import forms

class KeywordForm(forms.Form):
    title = forms.CharField(max_length=255)