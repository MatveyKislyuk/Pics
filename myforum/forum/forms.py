# forum/forms.py
from django import forms
from .models import Image, Tag

class ImageForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False,label="Теги", help_text='Введите теги через запятую')
    title = forms.CharField(label="Заголовок", max_length=255)
    image = forms.ImageField(label="Изображение")
    class Meta:
        model = Image
        fields = ['title', 'image', 'tags']

    def save(self, commit=True):
        image = super(ImageForm, self).save(commit=False)

        # Сохраняем изображение, чтобы получить идентификатор (id)
        if commit:
            image.save()

        tag_names = [tag.strip() for tag in self.cleaned_data['tags'].split(',') if tag.strip()]

        image.tags.clear()
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            image.tags.add(tag)

        if commit:
            image.save()
        return image

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class AddTagForm(forms.ModelForm):
    new_tag = forms.CharField(required=False)

    class Meta:
        model = Tag
        fields = ['name']

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)