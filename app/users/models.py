'''
Models for core APIs
'''
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class TierList(models.TextChoices):
    '''Choices for user's account tier'''
    CUSTOM = 'CUSTOM', 'Custom'
    BASIC = 'BASIC', 'Basic'
    PREMIUM = 'PREMIUM', 'Premium'
    ENTERPRISE = 'ENTERPRISE', 'Enterprise'

    @classmethod
    def get_available_sizes(cls, user):
        if user.tier == cls.CUSTOM:
            return user.custom_tier.thumbnail_sizes
        mapped_thumb_sizes = {
            cls.BASIC.value: [200],
            cls.PREMIUM.value: [200, 400],
            cls.ENTERPRISE.value: [200, 400]
        }
        return mapped_thumb_sizes[user.tier]


class UserManager(BaseUserManager):
    ''' Manager for user model '''

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class Tier(models.Model):
    thumbnail_sizes = ArrayField(
        models.IntegerField(validators=[MinValueValidator(1)]))
    original_file_access = models.BooleanField()
    binary_file_access = models.BooleanField()


class User(AbstractBaseUser, PermissionsMixin):
    ''' User model in system '''
    email = models.EmailField(
        max_length=255, blank=True, null=True, default=None, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    tier = models.CharField(
        max_length=255, choices=TierList.choices, default=TierList.BASIC)
    custom_tier = models.ForeignKey(
        Tier, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(Q(tier=TierList.CUSTOM, custom_tier__isnull=False)) |
                (Q(tier=TierList.BASIC, custom_tier__isnull=True)) |
                (Q(tier=TierList.PREMIUM, custom_tier__isnull=True)) |
                (Q(tier=TierList.ENTERPRISE, custom_tier__isnull=True)),
                name='%(class)s_check_custom_tier'),
        ]

    def is_access_to_original_image(self):
        if self.tier in [TierList.ENTERPRISE, TierList.PREMIUM]:
            return True
        elif self.tier == TierList.CUSTOM and self.custom_tier.original_file_access:
            return True
        return False

    def is_access_to_binary_image(self):
        if self.tier in [TierList.ENTERPRISE]:
            return True
        elif self.tier == TierList.CUSTOM and self.custom_tier.binary_file_access:
            return True
        return False
