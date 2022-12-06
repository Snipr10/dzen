from django.db import models
from datetime import datetime
import pytz
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.id


class DzenUser(models.Model):
    id = models.IntegerField(primary_key=True)
    screen_name = models.CharField(max_length=255)
    followers = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=now, blank=True, null=True)
    sphinx_id = models.CharField(max_length=4096)
    name = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    last_modified = models.DateTimeField(default=now, blank=True, null=True)
    # is_verified = models.BooleanField(default=0)
    url = models.CharField(max_length=4096)

    class Meta:
        db_table = 'prsr_parser_dzen_user'


class UserDescription(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    description = models.CharField(max_length=4096)
    last_modified = models.DateTimeField(default=now)

    class Meta:
        db_table = 'prsr_parser_dzen_user_description'


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    created_date = models.DateField(default=datetime(1, 1, 1, 0, 0, tzinfo=pytz.UTC))
    owner_id = models.IntegerField()
    date_added = models.DateTimeField(default=now)
    likes = models.IntegerField(default=0)
    last_parsing = models.DateTimeField(default=datetime(1, 1, 1, 0, 0, tzinfo=pytz.UTC))
    taken = models.IntegerField(default=0)
    sphinx_id = models.CharField(max_length=4096)
    comments = models.IntegerField(default=0)
    content_hash = models.CharField(max_length=4096, default=None)
    last_modified = models.DateTimeField(default=now)
    url = models.CharField(max_length=4096)

    class Meta:
        db_table = 'prsr_parser_dzen_post'


class PostContent(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=10000)

    class Meta:
        db_table = 'prsr_parser_dzen_post_content'


class PostImage(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.CharField(max_length=10000)

    class Meta:
        db_table = 'prsr_parser_dzen_post_image'
