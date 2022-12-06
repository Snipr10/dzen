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
    name = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    followers = models.IntegerField(default=0)
    found_date = models.DateTimeField(default=now, blank=True, null=True)
    last_modified = models.DateTimeField(default=now, blank=True, null=True)
    #
    # sphinx_id = models.CharField(max_length=4096)
    # # is_verified = models.BooleanField(default=0)

    class Meta:
        db_table = 'prsr_parser_dzen_user'


class UserDescription(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    description = models.CharField(max_length=4096)
    url = models.CharField(max_length=4096)

    class Meta:
        db_table = 'prsr_parser_dzen_user_description'


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    owner_id = models.IntegerField()
    created_date = models.DateField(default=datetime(1, 1, 1, 0, 0, tzinfo=pytz.UTC))
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    trust = models.IntegerField(default=0)
    content_hash = models.CharField(max_length=4096, default="")
    last_modified = models.DateTimeField(default=datetime(1, 1, 1, 0, 0, tzinfo=pytz.UTC))
    found_date = models.DateTimeField(default=now)


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
