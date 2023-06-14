import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Genre(models.Model):
    """The Genre model"""
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ["name"]


class Language(models.Model):
    """The Language model"""
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    """The Author model"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(verbose_name="Date of birth", null=True, blank=True)
    date_of_death = models.DateField(null=True, verbose_name="Died", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    class Meta:
        ordering = ['last_name', 'first_name']


class Book(models.Model):
    """The book model: Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=100, )
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="books")
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text='13 Characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, help_text='Select a genre for this book')
    language = models.OneToOneField(Language, on_delete=models.CASCADE, )
    pub_date = models.DateField(verbose_name="Published date")
    slug = models.SlugField(
        max_length=50, default="",
        blank=True, null=False,
        db_index=True,
        unique=True
    )

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    def get_summary(self):
        return

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the book model."""
        return reverse("book-detail-view", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# class User(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)


LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('o', 'On loan'),
    ('a', 'Available'),
    ('r', 'Reserved'),
)


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library'
    )
    due_return = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True, default='m',
        help_text='Book availability',
    )
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, )
    imprint = models.CharField(max_length=200)

    # borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)

    class Meta:
        ordering = ['due_return']

    def __str__(self):
        return f"{self.id} by {self.book.title}"
