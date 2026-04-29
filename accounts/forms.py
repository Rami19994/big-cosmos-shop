from django import forms
from django.contrib.auth.models import User

from accounts.models import Address, Profile, SavedPreference



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "avatar", "preferred_language", "preferred_currency", "marketing_opt_in"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["user"]


class SavedPreferenceForm(forms.ModelForm):
    class Meta:
        model = SavedPreference
        exclude = ["user"]
