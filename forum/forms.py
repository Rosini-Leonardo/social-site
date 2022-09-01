from django import forms
from .models import Post,Discussione


class DiscussioneModelForm(forms.ModelForm):
    contenuto = forms.CharField( 
        widget = forms.Textarea(
            attrs={ "placeholder":"di cosa vuoi parlarci?"}), 
            max_length=4000,
            label="Primo messaggio"
    )
    class Meta:
        model = Discussione
        fields = ["titolo","contenuto"]
        widgets = {
            "titolo" : forms.TextInput(
                attrs={ "placeholder":"Titolo della discussione"}
            )
        }

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["contenuto"]
        widgets = {
            "contenuto": forms.Textarea(attrs={'rows':'5'})
        }
        labels = { "contenuto" : "Messaggio" }