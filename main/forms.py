from django import forms
from .models import Appointment, User, SpecializationCategory, Callback, Doctor, AppointmentTime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import DateInput


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))
    first_name = forms.CharField(label='First name',
                                 widget=forms.TextInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))
    last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))
    date_of_birth = forms.DateField(label='Date of birth', widget=DateInput(
        attrs={'class': 'reg-user', 'type': 'date', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}), initial=None, required=False)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))
    phone_number = forms.CharField(label='Phone number',
                                   widget=forms.TextInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))
    password2 = forms.CharField(label='Password repeat',
                                widget=forms.PasswordInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number', 'username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'reg-user', 'placeholder': '', 'style': 'font-family: "Inter"; font-size: 14px; font-weight: 500;'}))


class AppointmentForm(forms.ModelForm):
    day = forms.DateField(label='', widget=forms.TextInput(attrs={'type': 'date'}))
    time = forms.ModelChoiceField(queryset=AppointmentTime.objects.all(), label='', required=False)

    class Meta:
        model = Appointment
        fields = ['day', 'time']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Извлекаем пользователя из kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user  # Присваиваем пользователя экземпляру Appointment
        instance.appointment_day = self.cleaned_data['day']  # Сохраняем выбранную пользователем дату
        if commit:
            instance.save()
        return instance


class DoctorFilterForm(forms.Form):
    specialization = forms.ModelChoiceField(queryset=SpecializationCategory.objects.all(), label='',
                                            empty_label='All', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # .
        self.fields['specialization'].attrs = {'class': 'filter'}


class AppointmentDoctorFilterForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.none(), label='', widget=forms.Select(attrs={'class': 'custom-filter-field'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['doctor'].queryset = Doctor.objects.filter(appointments__user=user).distinct()


class CallbackForm(forms.ModelForm):
    class Meta:
        model = Callback
        fields = ('name', 'email', 'phone', 'date')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }