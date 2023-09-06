from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class products(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="products/")
    name = models.CharField(max_length=70)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class customeUserManager(BaseUserManager):

    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)
    
    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = customeUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def getInitial(self):
        return self.first_name[0].upper()
    

    

class country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Address(models.Model):
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    building_type = models.CharField(max_length=250)
    street_address = models.CharField(max_length=250)
    country = models.ForeignKey(country, null=True, on_delete=models.SET_NULL)

    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class orderItem(models.Model):
    product = models.ForeignKey(products, null=True, on_delete=models.SET_NULL)
    cumstomer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.cumstomer.first_name
    
    def Total(self):
        return self.quantity * self.product.price




