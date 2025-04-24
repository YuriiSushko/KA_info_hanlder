from django.db import models
from data_tracker.users.models import Mortals
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class SotialRole(models.Model):
    title = models.CharField(max_length=100, verbose_name="Роль")
    description = models.TextField(verbose_name="Опис")
    
    class Meta:
        verbose_name = "Соціальна роль"
        verbose_name_plural = "Соціальні ролі"
    
    def __str__(self):
        return self.title
    
class KaRole(models.Model):
    title = models.CharField(max_length=100, verbose_name="Роль")
    description = models.TextField(verbose_name="Опис")
    
    class Meta:
        verbose_name = "Роль відносно команди"
        verbose_name_plural = "Ролі відносно команди"
    
    def __str__(self):
        return self.title
    
class EventType(models.Model):
    title = models.CharField(max_length=225, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    
    class Meta:
        verbose_name = "Тип взаємодії"
        verbose_name_plural = "Типи взаємодії"
    
    def __str__(self):
        return self.title

class Institution(models.Model):
    name = models.CharField(max_length=225, verbose_name="Ім'я організації")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name="Номер телефону")
    email = models.EmailField(null=True, blank=True, verbose_name="Пошта")
    people = models.ManyToManyField("User", related_name="institutions", blank=True, verbose_name="Персони")
    role = models.ForeignKey(KaRole, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль відносно нас")
    contact_info = GenericRelation("ContactInfoInline", related_query_name='contact_info')
    
    class Meta:
        verbose_name = "Організація"
        verbose_name_plural = "Організації"
    
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    surname = models.CharField(max_length=100, verbose_name="Прізвище")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name="Номер телефону")
    email = models.EmailField(null=True, blank=True, verbose_name="Пошта")
    # institution = models.ForeignKey(Institution, null=True, blank=True, verbose_name="Організація")
    sotial_role = models.ForeignKey(SotialRole, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Соціальна роль")
    ka_role = models.ForeignKey(KaRole, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль відносно нас")
    contact_info = GenericRelation("ContactInfoInline", related_query_name='contact_info')
    
    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персони"
    
    def __str__(self):
        return f"{self.name} {self.surname}"

class Event(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name="Тип взаємодії")
    conductor = models.ForeignKey(Mortals, on_delete=models.CASCADE, verbose_name="Хто проводить")
    
    event_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата")
    
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Локація")
    outcome = models.CharField(max_length=255, blank=True, null=True, verbose_name="Підсумок")
    notes = models.TextField(blank=True, null=True, verbose_name="Нотатки")
    communication_channel = models.CharField(max_length=50, blank=True, null=True, verbose_name="Канал комунікації")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    
    class Meta:
        verbose_name = "Взаємодія"
        verbose_name_plural = "Взаємодії"
    
    def __str__(self):
        return f"{self.event_type} on {self.event_date}"

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='participant', verbose_name="Учасник")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Учасник")
    object_id = models.PositiveIntegerField()
    participant = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = "Учасник"
        verbose_name_plural = "Учасники"

class ContactInfoInline(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    value = models.CharField(max_length=225, blank=True, null=True, verbose_name="Додаткова контактна інформація")

    class Meta:
        verbose_name = "Додаткова контактна інформація"
        verbose_name_plural = "Додаткова контактна інформація"
    
    def __str__(self):
        return self.value