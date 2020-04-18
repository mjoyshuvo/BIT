from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, email, username, password=None):
        """Creates a new user profile."""
        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """Creates and saves a new superuser with given details."""
        user = self.create_user(email, username, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(null=False, blank=False, max_length=500)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_name(self):
        return self.name

    def get_username(self):

        return self.username

    def __str__(self):

        return self.email


class OauthCode(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    code = models.CharField(null=False, blank=False, max_length=100)
    access_token = models.CharField(null=True, blank=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SelectedRepos(models.Model):
    user = models.ForeignKey(UserProfile, null=False, blank=False, on_delete=models.PROTECT)
    repo_name = models.CharField(max_length=250, null=False, blank=False)
    stars = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
