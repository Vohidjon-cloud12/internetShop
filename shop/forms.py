from django import forms

from shop.models import Comment, Order


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ()
