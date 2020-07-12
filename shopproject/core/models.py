import uuid
from django.db import models
import os
import hashlib
import datetime
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html, mark_safe
from django.core.files.storage import FileSystemStorage
from uuslug import uuslug


class Timestamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Seo(models.Model):
    meta_description = models.TextField(
                                        help_text="Seo description",
                                        null=True, blank=True)
    meta_keywords = models.CharField(max_length=200,
                                     help_text="Comma separated keywords for page",
                                     null=True, blank=True)
    class Meta:
        abstract = True


class UUidModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class UUSlug(models.Model):
    slug = models.SlugField(max_length=50, unique=True,
        help_text='Unique value for page URL, created from name.')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        value = getattr(self, 'slug_field')
        self.slug = uuslug(getattr(self, value), instance=self)
        super().save(*args, **kwargs)


class Published(models.Model):
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise(Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(MediaFileSystemStorage, self)._save(name, content)


def get_upload_path(instance, filename):
    name = instance.__class__.__name__.lower()
    return os.path.join('{}_{}_{}/{}/{}'.format(
        datetime.datetime.now().day,
        datetime.datetime.now().month,
        datetime.datetime.now().year, name, filename))


class Media(models.Model):
    image = models.ImageField(upload_to=get_upload_path,
                              storage=MediaFileSystemStorage(), null=True, blank=True)
    caption = models.CharField(null=True, blank=True, max_length=100)
    md5sum = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        abstract = True

    def filename(self):
        return os.path.basename(self.image.name)

    def get_thumbnails(self):
        im = get_thumbnail(self.image, 'x500', quality=99)
        return im.url

    def get_thumb(self):
        if self.image:
            return format_html("<img src='{}' width='100' height='auto'>",
                               self.image.url)
        return ''

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.image.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)
