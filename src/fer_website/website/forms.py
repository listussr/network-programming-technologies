from django import forms

class RegistrationForm(forms.Form):
    login = forms.CharField(label="Логин", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), max_length=100)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}), max_length=100)
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class LoginForm(forms.Form):
    login = forms.CharField(label="Логин", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class ModelDatasetForm(forms.Form):
    model = forms.ChoiceField(choices=[
        ('', '-- Выберите модель --'),
        ('vgg_19', 'VGG-19'),
        ('resnet_18', 'ResNet-18'),
        ('densenet121', 'DenseNet121'),
        ('inception_v3', 'Inception-v3'),
    ])
    dataset = forms.ChoiceField(choices=[
        ('', '-- Выберите набор данных --'),
        ('fer2013', 'FER2013'),
        ('affectnet', 'AffectNet'),
    ])

class ModelForm(forms.Form):
    model = forms.ChoiceField(choices=[
        ('', '-- Выберите модель --'),
        ('vgg_19', 'VGG-19'),
        ('resnet_18', 'ResNet-18'),
        ('densenet121', 'DenseNet121'),
        ('inception_v3', 'Inception-v3'),
    ])

class DatasetForm(forms.Form):
    dataset = forms.ChoiceField(choices=[
        ('', '-- Выберите набор данных --'),
        ('fer2013', 'FER2013'),
        ('affectnet', 'AffectNet'),
    ])

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class DynamicTextForm(forms.Form):
    text = forms.CharField(label="Текст", required=False)

    def add_fields(self, extra_fields):
        for i in range(extra_fields):
            self.fields[f'text_{i}'] = forms.CharField(label=f"Текст {i + 1}", required=False)