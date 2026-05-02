from django import forms
from .models import ContactRequest

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'address', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон / WhatsApp'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email, если есть'}),
            'address': forms.TextInput(attrs={'placeholder': 'Город или адрес доставки'}),
            'message': forms.Textarea(attrs={'placeholder': 'Комментарий: размер, цвет, количество...', 'rows': 4}),
        }
