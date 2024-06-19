from django import forms

class CodeForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea, label='Ingrese el código aquí')