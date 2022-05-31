import uuid
from datetime import date
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    amount_owed = models.IntegerField(default=0)

    def __str__(self):
        return self.email


class Genre(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Format(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Format, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Language(models.Model):
    title = models.CharField(max_length=200, help_text="this is some default text")
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.last_name+'-'+self.first_name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)


class Item(models.Model):
    cover = models.ImageField(upload_to='book_covers')
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    publisher = models.CharField(max_length=255)
    creation_date = models.CharField(max_length=255)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre)
    copies = models.IntegerField()

    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ItemInstance(models.Model):
    STATUS_CHOICES = (
        ('Instance', 'Instance'),
        ('Hold', 'Hold'),
        ('Reserve', 'Reserve'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    due_date = models.DateField(null=True, blank=True)
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=30, default='Instance', choices=STATUS_CHOICES)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.id) + '-' + str(self.item))
        super(ItemInstance, self).save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.due_date and date.today() > self.due_date:
            return True
        return False

    def __str__(self):
        return '{0} ({1})'.format(str(self.id), str(self.item))
