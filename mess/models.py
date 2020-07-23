from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#Custom User Model
class StudentManager(BaseUserManager):

    def create_user(self, firstname, lastname, mobile, room, password=None):

        if not firstname:
            raise ValueError('Users must have an first name')

        if not lastname:
            raise ValueError('Users must have an last name')

        if not mobile:
            raise ValueError('Users must have an mobile number')

        if not room:
            raise ValueError('Users must have an room number')

        user = self.model(
            firstname = firstname,
            lastname = lastname,
            mobile = mobile,
            room = room,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, lastname, mobile, room="ADMIN", password=None):

        user = self.create_user(
            firstname = firstname,
            lastname = lastname,
            mobile = mobile,
            room = room,
            password = password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Student(AbstractBaseUser):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    #email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    mobile = PhoneNumberField(null=False, blank=False, unique=True)
    room = models.CharField(max_length=7)
    joiningdate = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return (self.firstname + " " + self.lastname + " " + str(self.mobile))

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

