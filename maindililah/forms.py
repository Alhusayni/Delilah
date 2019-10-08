from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from maindililah.models import UsersReview


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class ReviewForm(forms.Form):
    CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),)
    review = forms.CharField(widget=forms.Textarea)
    Streets_Quality = forms.ChoiceField(choices=CHOICES)
    Traffic = forms.ChoiceField(choices=CHOICES)
    Public_Schools = forms.ChoiceField(choices=CHOICES)
    Outdoor_Activities = forms.ChoiceField(choices=CHOICES)
