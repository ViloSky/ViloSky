'''Forms for the ViloSky app'''
import datetime
from django import forms
from ViloSkyApp.models import (UserProfile, Qualification, AdminInput, DropdownAdminInput,
                               TextAdminInput, TextareaAdminInput, CheckboxAdminInput)
from django.contrib.auth import get_user_model


class UserForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control txtbox'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control txtbox'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control txtbox'}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'confirm_password')


class UserProfileForm(forms.ModelForm):
    cur_year = datetime.datetime.today().year
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(
        years=tuple([i for i in range(cur_year - 80, cur_year - 16)])))
    #company = forms.CharField(widget=forms.TextInput())
    #employment_status = forms.CharField(max_length = 1, widget = forms.Select(choices=UserProfile.EmploymentStatusTypes))
    #employment_status = forms.CharField()
    #employment_sector = forms.CharField(widget=forms.TextInput())
    #time_worked_in_industry = forms.Select(choices=UserProfile.TimeWorkedTypes)

    class Meta:
        model = UserProfile
        fields = (
            'date_of_birth',
            'company',
            'employment_sector',
            'employment_status',
            'time_worked_in_industry'
        )


class QualificationForm(forms.ModelForm):
    level = forms.CharField(max_length=160, widget=forms.TextInput(attrs={
        'placeholder': 'Level e.g. High School ',
    }),
        required=True)
    subjects = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Subject',
    }),
        required=True)

    class Meta:
        model = Qualification
        fields = (
            'level',
            'subjects'
        )
# QualificationFormSet = modelformset_factory(QualificationForm, fields = ('user','level', 'subjects'), extra = 1)


class DropdownAdminInputForm(forms.ModelForm):
    choices = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = DropdownAdminInput
        fields = [
            'label',
            'is_required',
            'choices',
        ]


class CheckboxAdminInputForm(forms.ModelForm):

    class Meta:
        model = CheckboxAdminInput
        fields = [
            'label',
            'is_required',
            'default_value',
        ]


class TextAdminInputForm(forms.ModelForm):

    class Meta:
        model = TextAdminInput
        fields = [
            'label',
            'is_required',
            'max_length',
        ]


class TextareaAdminInputForm(forms.ModelForm):

    class Meta:
        model = TextareaAdminInput
        fields = [
            'label',
            'is_required',
            'max_length',
        ]
