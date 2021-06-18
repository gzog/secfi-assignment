from django import forms
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


class UserCreateForm(UserForm):
    pass


class UserUpdateForm(UserForm):
    password = forms.CharField(
        min_length=8,
        max_length=255,
        required=False,
    )
