import json

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from six import python_2_unicode_compatible

# Create your models here.

BOOK_PUBLISHING_STATUS_PUBLISHED = 'published'
BOOK_PUBLISHING_STATUS_NOT_PUBLISHED = 'not_published'
BOOK_PUBLISHING_STATUS_IN_PROGRESS = 'in_progress'
BOOK_PUBLISHING_STATUS_CANCELLED = 'cancelled'
BOOK_PUBLISHING_STATUS_REJECTED = 'rejected'
BOOK_PUBLISHING_STATUS_CHOICES = (
    (BOOK_PUBLISHING_STATUS_PUBLISHED,"Published"),
    (BOOK_PUBLISHING_STATUS_NOT_PUBLISHED,"Not Published"),
    (BOOK_PUBLISHING_STATUS_IN_PROGRESS,"In progress"),
    (BOOK_PUBLISHING_STATUS_CANCELLED,"Rejected"),
)
BOOK_PUBLISHING_STATUS_DEFAULT = BOOK_PUBLISHING_STATUS_PUBLISHED

@python_2_unicode_compatible
class Publisher(models.Model):
    """Publisher"""
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    website = models.URLField()
    latitude = models.DecimalField(null=True, blank=True, decimal_places=15,max_digits=19,default=0)
    longitude = models.DecimalField(null=True, blank=True, decimal_places=15, max_digits=19, default=0)

    class Meta(object):
        """Meta Options"""
        ordering = ["id"]

    def __str__(self):
        return self.name

    def location_field_indexing(self):
        """Location for indexing. Used in Elasticsearch indexing/tests of 'geo_distance' native filter."""
        return {
            'lat': self.latitude,
            'lon': self.longitude,
        }

@python_2_unicode_compatible
class Author(models.Model):
    """Author"""
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='authors', null=True, blank=True)

    class Meta(object):
        """Meta Options"""
        ordering = ["id"]

    def __str__(self):
        return self.name

class Tag(models.Model):
    """Simple Tag Model"""
    title = models.CharField(max_length=255, unique=True)

    class Meta(object):
        """Meta Options"""
        verbose_name = _("Tag")
        verbose_name = _("Tags")

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class Book(models.Model):
    """Books"""
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField('books.Author', related_name='books')
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete = models.CASCADE)
    publication_date = models.DateField()
    state = models.CharField(max_length=100, choices=BOOK_PUBLISHING_STATUS_CHOICES, default=BOOK_PUBLISHING_STATUS_DEFAULT)
    isbn = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.PositiveIntegerField(default=200)
    stock_count = models.PositiveIntegerField(default=30)
    tags = models.ManyToManyField('books.Tag', related_name='books', blank=True)

    class Meta(object):
        """Meta Options"""
        ordering = ["isbn"]

    def __str(self):
        return self.title

    @property
    def publisher_indexing(self):
        """Publisher for indexing. Used in ElasticSearch Indexing"""
        if self.publisher is not None:
            return self.publisher.name

    @property
    def tags_indexing(self):
        """Tags for indexing. Used in Elasticsearch indexing."""
        return [tag.title for tag in self.tags.all()]
