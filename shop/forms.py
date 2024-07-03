from django import forms

from shop.models import Comment, Order, Product, CustomUser


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'email', 'quantity')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email or password is incorrect')
        else:
            return email

    def clean_password(self):
        password = self.cleaned_data['password']
        email = self.clean_email()
        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError('Email or password is incorrect')
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('Email or password is incorrect')
        return password


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            return email
        else:
            raise forms.ValidationError('User with this email is already registered')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data
