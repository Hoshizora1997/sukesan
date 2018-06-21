from django import forms
from core.models import UserData,Mob,PlanDetail,Plan
from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class PlanForm(forms.ModelForm):
    MINUTES_CHOICES = (
        (0, '00分'),
        (1, '15分'),
        (2, '30分'),
        (3, '45分')
    )

    #title = forms.CharField(widget=forms.TextInput)
    #description = forms.TimeField(widget=forms.Textarea)
    #place = forms.CharField(widget=forms.TextInput)
    hours = forms.IntegerField(widget=forms.NumberInput)
    minutes = forms.ChoiceField(widget=forms.Select, choices=MINUTES_CHOICES)
    startDate = forms.DateField(widget=AdminDateWidget)
    endDate = forms.DateField(widget=AdminDateWidget)
    startTimeHours = forms.IntegerField(widget=forms.NumberInput)
    startTimeMinutes = forms.ChoiceField(widget=forms.Select, choices=MINUTES_CHOICES)
    endTimeHours = forms.IntegerField(widget=forms.NumberInput)
    endTimeMinutes = forms.ChoiceField(widget=forms.Select, choices=MINUTES_CHOICES)

    class Meta:
        model = Plan
        fields = (
            'title', 'description', 'place','startDate','endDate'
        )

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['place'].widget.attrs['class'] = 'form-control'
        self.fields['hours'].widget.attrs['class'] = 'form-control'
        self.fields['minutes'].widget.attrs['class'] = 'form-control'
        self.fields['startDate'].widget.attrs['class'] = 'vDateField form-control'
        self.fields['endDate'].widget.attrs['class'] = 'vDateField form-control'
        self.fields['startTimeHours'].widget.attrs['class'] = 'form-control'
        self.fields['startTimeMinutes'].widget.attrs['class'] = 'form-control'
        self.fields['endTimeHours'].widget.attrs['class'] = 'form-control'
        self.fields['endTimeMinutes'].widget.attrs['class'] = 'form-control'


class MobForm(forms.ModelForm):
    class Meta:
        model = Mob
        fields = (
            'name',
        )

    def __init__(self, *args, **kwargs):
        super(MobForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
    # 入力を必須にするため、required=Trueで上書き
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username", "email", "password1", "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = '確認用パスワード'

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("正しいメールアドレスを指定してください。")

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise ValidationError("このメールアドレスは既に使用されています。別のメールアドレスを指定してください")


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名 or メールアドレス'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'