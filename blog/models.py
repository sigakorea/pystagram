import re
from uuid import uuid4
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from pystagram.validators import jpeg_validator
from pystagram.image import receiver_with_image_field
from pystagram.file import random_name_upload_to


def validate_hexstring(value):
    if not re.match(r'^[0-9a-fA-F]+$', value):
        raise ValidationError("hexstring이 아니오.")

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    uuid = models.UUIDField(default=uuid4, editable=False, db_index=True)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100, db_index=True) #, validators=[validate_hexstring])
    content = models.TextField()
    photo = models.ImageField(
        blank=True,
        null=True,
        validators=[jpeg_validator],
        upload_to=random_name_upload_to)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_posts')
    lnglat = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    origin_url = models.URLField(blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.pk]) #self.uuid.hex])


receiver = receiver_with_image_field('photo', 1024)
pre_save.connect(receiver, sender=Post)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Photograph(models.Model):
    #image_url = models.URLField()
    image_file = models.ImageField(upload_to='%Y/%m/%d/')
    description = models.TextField(null=True)
    tags = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(auto_now_add=True)
