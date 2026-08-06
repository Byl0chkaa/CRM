from core.enums.regex import RegexPhoneNumber
from django.core import validators as V
from django.db import models


class CourseModel(models.TextChoices):
    FS = 'FS'
    QACX = 'QACX'
    JCX = 'JCX'
    JSCX = 'JSCX'
    FE = 'FE'
    PCX = 'PCX'


class CourseFormatModel(models.TextChoices):
    STATIC = 'static'
    ONLINE = 'online'


class CourseTypeModel(models.TextChoices):
    PRO = 'pro'
    MINIMAL = 'minimal'
    PREMIUM = 'premium'
    INCUBATOR = 'incubator'
    VIP = 'vip'


class OrderStatusModel(models.TextChoices):
    INWORK = 'In work'
    NEW = 'New'
    AGREED = 'Agreed'
    DISAGREED = 'Disagreed'
    DUBBING = 'Dubbing'


class OrderModel(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    surname = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=17, validators=[
        V.RegexValidator(RegexPhoneNumber.PHONE_NUMBER.pattern, RegexPhoneNumber.PHONE_NUMBER.msg)], null=True,
                             blank=True)
    age = models.IntegerField(validators=[V.MinValueValidator(1), V.MaxValueValidator(100)], null=True, blank=True)
    course = models.CharField(max_length=5, choices=CourseModel.choices)
    course_format = models.CharField(max_length=6, choices=CourseFormatModel.choices)
    course_type = models.CharField(max_length=10, choices=CourseTypeModel.choices)
    status = models.CharField(max_length=9, choices=OrderStatusModel.choices, null=True, blank=True)
    sum = models.IntegerField(null=True, blank=True)
    alreadyPaid = models.IntegerField(null=True, blank=True)
    group=models.CharField(max_length=25, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    manager=models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-id']
