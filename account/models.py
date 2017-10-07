from django.db import models
from django.contrib.auth.hashers import (
    check_password, make_password,
)
from django.utils.translation import ugettext_lazy as _


class TaskUserManager(models.Manager):
    @classmethod
    def normalize_email(cls, email):
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        extra_fields.get('full_name', '')
        extra_fields.get('role', 3)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)


class TaskUser(models.Model):
    ROLE_TYPE = {
        (1, 'admin'),
        (2, 'teacher'),
        (3, 'student'),
    }
    email = models.EmailField(verbose_name=_('email address'),
                              max_length=255,
                              unique=True
                              )
    full_name = models.CharField(_('Full name'),
                                 max_length=150,
                                 blank=True,
                                 null=False
                                 )
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    email_verifed = models.BooleanField(default=False)
    email_verify_date = models.DateTimeField(null=True, blank=True)
    role = models.IntegerField(choices=ROLE_TYPE, default=3)
    is_active = models.BooleanField(_('active'), default=True)
    blocked = models.BooleanField(_('blocked'), default=False)
    created = models.DateTimeField(_('date of joining'), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = TaskUserManager()

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def short_name(self):
        return str.title(str(self.full_name.split()[0]))

    def last_name(self):
        l = str(self.full_name).split()
        return str.title(l[len(l)-1])

    def name(self):
        return str.title(self.full_name)
