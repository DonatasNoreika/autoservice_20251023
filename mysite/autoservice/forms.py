from django import forms
from .models import OrderComment, CustomUser, Order
from django.contrib.auth.forms import UserCreationForm

class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ['content']


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']


class OrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'status', 'deadline']
        widgets = {'deadline': forms.DateInput(attrs={'type': 'datetime-local'})}


