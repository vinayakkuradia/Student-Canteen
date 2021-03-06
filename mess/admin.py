from django import forms
from django.contrib import admin
from django.forms import ModelForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from mess.models import Order
from mess.models import Student

##########Custom User Model Configurations##########

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ('firstname', 'lastname', 'mobile', 'room')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Student
        fields = ('firstname', 'lastname', 'mobile', 'room', 'password', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('firstname', 'lastname', 'mobile', 'room', 'joiningdate', 'password', 'is_active', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('mobile', 'password',)}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'room',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('firstname', 'lastname', 'mobile', 'room', 'password1', 'password2'),
        }),
    )
    search_fields = ('firstname', 'lastname', 'mobile', 'room', 'joiningdate',)
    ordering = ('firstname', 'lastname', 'mobile', 'room',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Student, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

##########General Model Registration##########

class OrderCreationForm(ModelForm):
    class Meta:
        model = Order
        fields = ['plate_count', 'payment_method', 'meal_type']

class OrderAdmin(admin.ModelAdmin):
    list_display= ('order_id', 'ordered_by', 'datetime', 'plate_count', 'payment_method', 'meal_type', 'confirmation_status')
    list_filter = ('ordered_by', 'datetime','payment_method', 'meal_type', 'confirmation_status',)
    search_fields = ('ordered_by', 'datetime',)
    ordering = ('datetime', 'ordered_by', 'confirmation_status',)

# Register your models here.
admin.site.register(Order, OrderAdmin)