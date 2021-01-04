import uuid
from django.db import models
from django.core.validators import MaxValueValidator
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

# Database Models

payment_methods = ((1, 'Cash'), (2, 'PayTM/GPay'), (3, 'Credit'),)
meal_types = ((1, 'Lunch'), (2, 'Dinner'),)

class Order(models.Model):
    order_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    ordered_by = models.ForeignKey(Student, blank=False, null=False, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    plate_count = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    payment_method = models.PositiveIntegerField(choices=payment_methods)
    meal_type = models.PositiveIntegerField(choices=meal_types)
    confirmation_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_id)











