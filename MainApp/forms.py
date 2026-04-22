from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Skill, Review


FORM_CONTROL_ATTRS = {'class': 'form-control'}
FORM_SELECT_ATTRS = {'class': 'form-select'}
FORM_CHECKBOX_ATTRS = {'class': 'form-check-input'}


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            **FORM_CONTROL_ATTRS,
            'placeholder': 'Email address',
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({**FORM_CONTROL_ATTRS, 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({**FORM_CONTROL_ATTRS, 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({**FORM_CONTROL_ATTRS, 'placeholder': 'Confirm password'})


class SkillForm(forms.ModelForm):
    free = forms.BooleanField(
        required=False,
        label='Free offer',
        widget=forms.CheckboxInput(attrs=FORM_CHECKBOX_ATTRS),
        help_text='Check this if you are offering the skill for free.',
    )

    class Meta:
        model = Skill
        fields = [
            'title',
            'description',
            'category',
            'price',
            'free',
            'contact_preference',
            'availability_status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={**FORM_CONTROL_ATTRS, 'placeholder': 'What skill are you offering?'}),
            'description': forms.Textarea(attrs={**FORM_CONTROL_ATTRS, 'rows': 5, 'placeholder': 'Describe your skill or service'}),
            'category': forms.Select(attrs=FORM_SELECT_ATTRS),
            'price': forms.NumberInput(attrs={**FORM_CONTROL_ATTRS, 'placeholder': 'Leave blank if free'}),
            'contact_preference': forms.Select(attrs=FORM_SELECT_ATTRS),
            'availability_status': forms.Select(attrs=FORM_SELECT_ATTRS),
        }

    def clean(self):
        cleaned_data = super().clean()
        free = cleaned_data.get('free')
        price = cleaned_data.get('price')

        if free:
            cleaned_data['price'] = None
        elif price is None:
            self.add_error('price', 'Enter a price or select Free offer.')

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs=FORM_SELECT_ATTRS),
            'comment': forms.Textarea(attrs={**FORM_CONTROL_ATTRS, 'rows': 3, 'placeholder': 'Write your review here...'}),
        }
