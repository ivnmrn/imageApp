from django import forms

class Image(forms.Form):
    file = forms.ImageField(label='')
