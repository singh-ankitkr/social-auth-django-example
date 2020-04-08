from django.db import models
from django.contrib.auth.models import User


class GitHubProfile(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile = models.CharField(max_length=12, unique=True)
    github_profile = models.OneToOneField(GitHubProfile, on_delete=models.CASCADE, null=True)  # allow nulls as well

    # linkedin = models.OneToOneField()  # allow nulls as well
    # twitter = models.OneToOneField()  # allow nulls as well

    class Meta:
        indexes = [models.Index(fields=['email']), ]


