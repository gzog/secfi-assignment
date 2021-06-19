import requests
from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password


def validate_digits_letters(word):
    for char in word:
        if not char.isdigit() and not char.isalpha():
            return False
    return True


class UserForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=255)
    password = forms.CharField(
        min_length=8,
        max_length=255,
        required=True,
    )
    last_name = forms.CharField(max_length=255)
    avatar = forms.CharField(max_length=1024)

    def clean_password(self):
        return make_password(self.cleaned_data["password"])

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not data.islower():
            raise forms.ValidationError("Username should be in lowercase")

        if not validate_digits_letters(data):
            raise forms.ValidationError(
                "Username contains characters that are not numbers nor letters"
            )

        return data

    def clean_avatar(self):
        url = f"https://api.imgbb.com/1/upload?key={settings.IMG_BB_API_KEY}"
        data = self.cleaned_data["avatar"]
        response = requests.post(url, {"image": data})
        response.raise_for_status()

        body = response.json()

        return body['data']['display_url']
