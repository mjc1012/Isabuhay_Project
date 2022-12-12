from decimal import Decimal
from django.urls import reverse
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime, timedelta, date
from django.utils import timezone
import pytz
# from traitlets import default
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, firstname, lastname, phone_number, password=None):
        if not username: raise ValueError("Username is required")
        if not email: raise ValueError("Email is required")
        if not firstname: raise ValueError("Firstname is required")
        if not lastname: raise ValueError("Lastname is required")
        if not phone_number: raise ValueError("Phone_number is required")

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            phone_number = phone_number
        )
        user.date_created = date.today()
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, firstname, lastname, phone_number, password=None):
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            phone_number = phone_number
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.date_created = date.today()
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length=25, blank=False, null=False, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=50, blank=False, null=False, unique=True)
    firstname = models.CharField(verbose_name="first name", max_length=20, blank=False, null=False)
    lastname = models.CharField(verbose_name="last name", max_length=20, blank=False, null=False)
    phone_number = models.CharField(verbose_name="phone number", max_length=15, blank=False, null=False)

    profile_picture = models.ImageField(verbose_name="profile picture", null=True, blank=True)
    birthdate = models.DateTimeField(verbose_name="birthdate", blank=True, null=True)
    blood_type = models.CharField(verbose_name="blood type", max_length=5, blank=True, null=True)
    height = models.DecimalField(verbose_name="height", decimal_places = 2, max_digits = 6, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    weight = models.DecimalField(verbose_name="weight", decimal_places = 2, max_digits = 6, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(verbose_name="date created", blank=True, null=True)

    uploads = models.IntegerField(verbose_name="uploads",blank=False, null=False, default=5)

    USERNAME_FIELD="username"

    REQUIRED_FIELDS = [
        'email',
        'firstname',
        'lastname',
        'phone_number',
    ]

    objects = UserManager()
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

# class Client


# Marc John Corral

class CBCTestResultImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    testImage = models.ImageField(verbose_name="testImage", blank=False, null=False)

    def get_id(self):
        return self.id
    
    def get_testImage(self):
        return self.testImage
    
    def set_testImage(self, value):
        self.testImage = value

class CBCTestResultPDF(models.Model):
    id = models.BigAutoField(primary_key=True)
    testPDF = models.FileField(verbose_name="testPDF", blank=False, null=False)

    def get_id(self):
        return self.id
    
    def get_testPDF(self):
        return self.testPDF
    
    def set_testPDF(self, value):
        self.testPDF = value

class CBCTestResultDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    testDocx = models.FileField(verbose_name="testDocx", blank=False, null=False)

    def get_id(self):
        return self.id
    
    def get_testDocx(self):
        return self.testDocx
    
    def set_testDocx(self, value):
        self.testDocx = value

class Promo(models.Model):
    id = models.BigAutoField(primary_key=True)
    uploads = models.IntegerField(blank=False, null=False)
    price = models.FloatField(blank=False, null=False)

    def get_id(self):
        return self.id

    def get_uploads(self):
        return self.uploads
    
    def set_uploads(self, value):
        self.uploads = value
    
    def get_price(self):
        return self.price
    
    def set_price(self, value):
        self.price = value


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def current_time():
        return timezone.now() + timezone.timedelta(hours=8)

    def get_id(self):
        return self.id

    def get_promo(self):
        return self.promo
    
    def set_promo(self, value):
        self.promo = value
    
    def get_user(self):
        return self.user
    
    def set_user(self, value):
        self.user = value
    
    def get_date(self):
        return self.date
    
    def set_date(self, value):
        self.date = value
    
class CBCTestResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    testImage = models.OneToOneField(CBCTestResultImage, on_delete=models.CASCADE, blank=True, null=True)
    testPDF = models.OneToOneField(CBCTestResultPDF, on_delete=models.CASCADE, blank=True, null=True)
    testDocx = models.OneToOneField(CBCTestResultDocument, on_delete=models.CASCADE, blank=True, null=True)
    source = models.CharField(max_length=50, blank=False, null=False)
    labNumber = models.CharField(max_length=50, blank=False, null=False)
    pid = models.CharField(max_length=50, blank=False, null=False)
    dateRequested = models.DateTimeField(blank=True, null=True)
    dateReceived = models.DateTimeField(blank=True, null=True)
    whiteBloodCells = models.FloatField(blank=False, null=False)
    redBloodCells = models.FloatField(blank=False, null=False)
    hemoglobin = models.FloatField(blank=False, null=False)
    hematocrit = models.FloatField(blank=False, null=False)
    meanCorpuscularVolume = models.FloatField(blank=False, null=False)
    meanCorpuscularHb = models.FloatField(blank=False, null=False)
    meanCorpuscularHbConc = models.FloatField(blank=False, null=False)
    rbcDistributionWidth = models.FloatField(blank=False, null=False)
    plateletCount = models.FloatField(blank=False, null=False)
    neutrophils = models.FloatField(blank=False, null=False)
    lymphocytes = models.FloatField(blank=False, null=False)
    monocytes = models.FloatField(blank=False, null=False)
    eosinophils = models.FloatField(blank=False, null=False)
    basophils = models.FloatField(blank=False, null=False)
    bands = models.FloatField(blank=False, null=False)
    absoluteNeutrophilsCount = models.FloatField(blank=False, null=False)
    absoluteLymphocyteCount = models.FloatField(blank=False, null=False)
    absoluteMonocyteCount = models.FloatField(blank=False, null=False)
    absoluteEosinophilCount = models.FloatField(blank=False, null=False)
    absoluteBasophilCount = models.FloatField(blank=False, null=False)
    absoluteBandCount = models.FloatField(blank=False, null=False)

    def get_id(self):
        return self.id

    def get_user(self):
        return self.user
    
    def set_user(self, value):
        self.user = value
    
    def get_testImage(self):
        return self.testImage
    
    def set_testImage(self, value):
        self.testImage = value
    
    def get_testPDF(self):
        return self.testPDF
    
    def set_testPDF(self, value):
        self.testPDF = value
    
    def get_testDocx(self):
        return self.testDocx
    
    def set_testDocx(self, value):
        self.testDocx = value
        
    def get_source(self):
        return self.source
    
    def set_source(self, value):
        self.source = value
    
    def get_labNumber(self):
        return self.labNumber
    
    def set_labNumber(self, value):
        self.labNumber = value
    
    def get_pid(self):
        return self.pid
    
    def set_pid(self, value):
        self.pid = value
    
    def get_dateRequested(self):
        return self.dateRequested
    
    def set_dateRequested(self, value):
        self.dateRequested = value
    
    def get_dateReceived(self):
        return self.dateReceived
    
    def set_dateReceived(self, value):
        self.dateReceived = value
    
    def get_whiteBloodCells(self):
        return self.whiteBloodCells
    
    def set_whiteBloodCells(self, value):
        self.whiteBloodCells = value
    
    def get_redBloodCells(self):
        return self.redBloodCells
    
    def set_redBloodCells(self, value):
        self.redBloodCells = value
    
    def get_hemoglobin(self):
        return self.hemoglobin
    
    def set_hemoglobin(self, value):
        self.hemoglobin = value
    
    def get_hematocrit(self):
        return self.hematocrit
    
    def set_hematocrit(self, value):
        self.hematocrit = value
    
    def get_meanCorpuscularVolume(self):
        return self.meanCorpuscularVolume
    
    def set_meanCorpuscularVolume(self, value):
        self.meanCorpuscularVolume = value
    
    def get_meanCorpuscularHb(self):
        return self.meanCorpuscularHb
    
    def set_meanCorpuscularHb(self, value):
        self.meanCorpuscularHb = value
    
    def get_meanCorpuscularHbConc(self):
        return self.meanCorpuscularHbConc
    
    def set_meanCorpuscularHbConc(self, value):
        self.meanCorpuscularHbConc = value
    
    def get_rbcDistributionWidth(self):
        return self.rbcDistributionWidth
    
    def set_rbcDistributionWidth(self, value):
        self.rbcDistributionWidth = value
    
    def get_plateletCount(self):
        return self.plateletCount
    
    def set_plateletCount(self, value):
        self.plateletCount = value
    
    def get_neutrophils(self):
        return self.neutrophils
    
    def set_neutrophils(self, value):
        self.neutrophils = value
    
    def get_lymphocytes(self):
        return self.lymphocytes
    
    def set_lymphocytes(self, value):
        self.lymphocytes = value
    
    def get_monocytes(self):
        return self.monocytes
    
    def set_monocytes(self, value):
        self.monocytes = value
    
    def get_eosinophils(self):
        return self.eosinophils
    
    def set_eosinophils(self, value):
        self.eosinophils = value
    
    def get_basophils(self):
        return self.basophils
    
    def set_basophils(self, value):
        self.basophils = value
    
    def get_bands(self):
        return self.bands
    
    def set_bands(self, value):
        self.bands = value
    
    def get_absoluteNeutrophilsCount(self):
        return self.absoluteNeutrophilsCount
    
    def set_absoluteNeutrophilsCount(self, value):
        self.absoluteNeutrophilsCount = value
    
    def get_absoluteLymphocyteCount(self):
        return self.absoluteLymphocyteCount
    
    def set_absoluteLymphocyteCount(self, value):
        self.absoluteLymphocyteCount = value
    
    def get_absoluteMonocyteCount(self):
        return self.absoluteMonocyteCount
    
    def set_absoluteMonocyteCount(self, value):
        self.absoluteMonocyteCount = value
    
    def get_absoluteEosinophilCount(self):
        return self.absoluteEosinophilCount
    
    def set_absoluteEosinophilCount(self, value):
        self.absoluteEosinophilCount = value
    
    def get_absoluteBasophilCount(self):
        return self.absoluteBasophilCount
    
    def set_absoluteBasophilCount(self, value):
        self.absoluteBasophilCount = value
    
    def get_absoluteBandCount(self):
        return self.absoluteBandCount
    
    def set_absoluteBandCount(self, value):
        self.absoluteBandCount = value

class Room(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def get_id(self):
        return self.id
    
    def get_owner(self):
        return self.owner
    
    def set_owner(self, value):
        self.owner = value

class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    read = models.BooleanField(default=False)

    def current_time():
        return timezone.now() + timezone.timedelta(hours=8)

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
    
    def get_date(self):
        return self.date
    
    def set_date(self, value):
        self.date = value
    
    def get_user(self):
        return self.user
    
    def set_user(self, value):
        self.user = value
    
    def get_room(self):
        return self.room
    
    def set_room(self, value):
        self.room = value
    
    def get_read(self):
        return self.read
    
    def set_read(self, value):
        self.read = value
    


# Marc John Corral
