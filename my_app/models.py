from datetime import datetime
from decimal import Decimal

from django.db import models
from django.core.validators import MinLengthValidator


class Book(models.Model):  # table name like <app_name>_<model_name>
    CATEGORY_CHOICES = [
        ('Fantasy', 'FANTASY CATEGORY'),
        ('Mystic', 'MYSTIC CATEGORY'),
        ('Biography', 'BIOGRAPHY CATEGORY'),
        ('N/A', 'UNRECOGNISED CATEGORY'),
    ]

    title: str = models.CharField(
        max_length=125,
        unique=True,
        verbose_name="Название книги",
        error_messages={  #  пересмотреть настройку параметра
            'blank': 'Сожалеем, но книгу нельзя создать без названия книги.',
            'unique': 'Кажется книга с таким названием уже существует.',
        }
    )
    description: str = models.TextField(
        verbose_name="Описание книги",
        validators=[
            MinLengthValidator(20),
            # MaxLengthValidator(500)
        ]
    )
    comment: str = models.TextField(
        null=True,
        blank=True,
        # unique_for_date='published_date'
        # unique_for_month='published_date'
        # unique_for_year='published_date'
    )
    published_date: datetime = models.DateTimeField(verbose_name="Дата публикации")
    price: Decimal = models.DecimalField(  # 123.45
        verbose_name="Цена книги",
        help_text="Цена книги в евро. Должно быть больше 0",
        max_digits=5,
        decimal_places=2,
        null=True,  #  сторона базы данных
        blank=True  #  сторона админ панели
    )
    category: str = models.CharField(
        verbose_name="Категория книги",
        help_text="Категория книги из списка предложенных. Если неизвестна, выберите 'N/A'",
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='N/A',
        # editable=False
    )
    # isbn: str = models.SlugField()



class Post(models.Model):
    title: str = models.CharField(
        max_length=200
    )
    content: str = models.TextField(
        validators=[
            MinLengthValidator(50)
        ]
    )

    # One to Many RelationShip
    author = models.ForeignKey(
        'Author',
        # on_delete=models.DO_NOTHING,  # при удалении родителя ничего не делай
        # on_delete=models.CASCADE,  # при удалении родителя удаляй все связанные записи КАСКАДНО
        on_delete=models.SET_NULL,  # обязательно требует включение null=True. При удалении родителя устанавливай значение NULL для всех его дочерних объектов
        # on_delete=models.SET_DEFAULT,  # обязательно требует включение default=<default value>. При удалении родителя устанавливай значение по умолчанию для всех его дочерних объектов
        # on_delete=models.PROTECT  # запретить удаление родителя, пока на него есть ХОТЬ ОДНА ССЫЛКА
        null=True,
        blank=True,
        related_name='posts'
    )

    created_at: datetime = models.DateTimeField(
        auto_now_add=True
    )


# Post.author -> -> Author obj.
# Author.posts -> ->  [Post obj, ... Post obj]

class Author(models.Model):
    username: str = models.CharField(
        max_length=30,
        unique=True
    )
    first_name: str = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    last_name: str = models.CharField(
        max_length=25,
        null=True,
        blank=True
    )


class AuthorProfile(models.Model):
    about: str = models.TextField(
        null=True
    )
    personal_website: str = models.URLField(
        max_length=255,
        null=True,
        blank=True
    )
    avatar: str = models.ImageField(
        upload_to='avatars/'
    )

    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='profile'
    )
