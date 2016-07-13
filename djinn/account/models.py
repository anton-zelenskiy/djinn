from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import date
from city.models import City


class ExtUserManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        if not email:
            raise ValueError('Email адрес является обязательным')
        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class ExtUser(AbstractBaseUser):
    email = models.EmailField('Email', unique=True, db_index=True)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    birth_date = models.DateField(null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=1)
    phone = models.CharField(max_length=20, null=True)
    skype = models.CharField(max_length=30, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField('Администратор', default=False)
    is_active = models.BooleanField('Активный', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = ExtUserManager()

    class Meta:
        db_table = 'account_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        if self.is_active and self.is_admin:
            return True

    def get_age(self):
        today = date.today()
        try:
            birthday = self.birth_date.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.birth_date.replace(year=today.year, month=self.birth_date.month + 1, day=1)
        if birthday > today:
            return today.year - self.birth_date.year - 1
        else:
            return today.year - self.birth_date.year

    @property
    def get_age_and_postfix(self):
        age = self.get_age()
        tmp1 = age % 10
        tmp2 = age % 100
        result = 'год' if tmp1 == 1 and tmp2 != 11 else \
                 'года' if (2 <= tmp1 <= 4) and (tmp2 < 10 or tmp2 >= 20) else \
                 'лет'
        return '%s %s' % (age, result)

    @property
    def is_staff(self):
        return self.is_admin
