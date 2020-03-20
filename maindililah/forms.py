from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from maindililah.models import UsersReview, ReplyReview, UserProfile, ReportReview
from captcha.fields import ReCaptchaField


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField()

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']
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
    Public_Transportation = forms.ChoiceField(choices=CHOICES)
    Traffic = forms.ChoiceField(choices=CHOICES)
    Public_Schools = forms.ChoiceField(choices=CHOICES)
    Outdoor_Activities = forms.ChoiceField(choices=CHOICES)
    captcha = ReCaptchaField()


class CompareCat(forms.Form):
    CPrice = (('0', 'Low Price'), ('1', 'High Price'))
    CPopulation = (('0', 'Fewer People'), ('1', 'More People'))
    Price = forms.ChoiceField(choices=CPrice)
    Population = forms.ChoiceField(choices=CPopulation)


class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField()


class EditProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'neighborhood', 'preferences_pop', 'preferences_price', 'profile_picture']


class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ReportForm(forms.Form):
    report = forms.CharField(widget=forms.Textarea)
