from django.db import models


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

    def __str__(self):
        return self.username

    class Meta:
        db_table = "authors"
        ordering = ["username",]

        permissions = [
            #  само разрешение    Визуальное отображение в админ панели
            ('can_get_statistic', 'Can Get Statistic'),
        ]


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
        upload_to='avatars/',
        null=True,
        blank=True
    )

    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    def __str__(self):
        # Сперва система получает все данные (SELECT * FROM '<AuthorProfile>')

        # При обращении к author.username, система пойдёт на +1 запрос (SELECT * FROM '<Author> WHERE id = <%s>')
        return self.author.username

    class Meta:
        db_table = "author_profiles"
