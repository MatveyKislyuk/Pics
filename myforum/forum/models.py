from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
