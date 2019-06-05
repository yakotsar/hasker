from django import forms
from hasker.models import Question

class AskForm(forms.Form):

    title = forms.CharField(
            max_length=255,
            widget = forms.TextInput(attrs={'class': 'form-control'}),
    )

    text = forms.CharField(
            max_length=500,
            label="Text",
            widget = forms.Textarea(attrs={'class': 'form-control'}),
    )

    tags = forms.CharField(
            max_length=100,
            label="Tags",
            widget = forms.TextInput(attrs={'class': 'form-control'}),
    )
