from django import forms
from accounts.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='Пароль должен содержать не менее 8 символов.'
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput,
        help_text='Введите тот же пароль для повторного подтверждения.'
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        initial='renter',
        label='Роль'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    pass
