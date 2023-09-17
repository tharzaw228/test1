from django import forms
from .models import Listing

class CreatListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'price', 'active', 'owner',  'category']