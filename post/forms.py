from django import forms
from django.contrib.auth.models import User

from django_summernote.fields import SummernoteTextFormField

from .models import Post
from .validators import LetterUsernameValidator


class LoginForm(forms.Form):
    """Форма авторизации"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} в системе не найден.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль.')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    """Форма регистрации"""
    username_validator = LetterUsernameValidator()
    username = forms.CharField(
        widget=forms.TextInput,
        max_length=15,
        min_length=3,
        help_text='Required. 15 characters or fewer. Letters, digits and _ only.',
        validators=[username_validator]
    )
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=12)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    email = forms.EmailField(help_text='Enter the valid email like "example@gmail.com".')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердить пароль'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Email {email} уже используется в системе.')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают.')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')


class EditProfileForm(RegistrationForm):
    """Форма для изменения данных в профиле"""
    bio = forms.CharField(widget=forms.Textarea, required=False, max_length=300)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['bio'].label = 'Краткая информация'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            if User.objects.get(username=username) != self.user:
                raise forms.ValidationError(f'Пользователь с логином {username} уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            if User.objects.get(email=email) != self.user:
                raise forms.ValidationError(f'Email {email} уже используется в системе.')
        return email

    class Meta(RegistrationForm.Meta):
        fields = ('username', 'password', 'confirm_password', 'email', 'first_name', 'last_name', 'bio')


class CreatePostForm(forms.ModelForm):
    """Форма для написания поста"""
    content = SummernoteTextFormField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название'
        self.fields['description'].label = 'Описание'
        self.fields['image_thumbnail'].label = 'Изображение'
        self.fields['tags'].label = 'Теги (категории)'
        self.fields['content'].label = 'Текст'

    def clean(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError('Пост с таким названием уже существует')

    class Meta:
        model = Post
        fields = ('title', 'description', 'image_thumbnail', 'content', 'tags')


class EditPostForm(CreatePostForm):
    """Форма для редактирования постов"""

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.fields['image_thumbnail'].required = False

    def clean(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title).exists():
            if Post.objects.get(title=title) != self.post:
                raise forms.ValidationError('Пост с таким названием уже существует')
