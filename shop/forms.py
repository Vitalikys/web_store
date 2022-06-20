from django import forms

from shop.models import OrderItem


class AddQuantityForm(forms.ModelForm):
    # quantity = forms.ModelChoiceField(widget = forms.ModelChoiceField(attrs={'class': 'form-control'}))
    class Meta:
        model = OrderItem
        fields = ['quantity']