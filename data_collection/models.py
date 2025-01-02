from django.db import models
import random
import string
from django.contrib.auth.hashers import make_password, check_password
from datetime import date

class Member(models.Model):
    agent_code = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    voter_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    education_background = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    ndc_membership_status = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)  # Add this field

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.agent_code}"
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def age(self):
        if self.birthdate:
            today = date.today()
            age = today.year - self.birthdate.year
            if today.month < self.birthdate.month or (today.month == self.birthdate.month and today.day < self.birthdate.day):
                age -= 1
            return age
        return None

    def generate_agent_code(self):
        while True:
            code = 'AG' + ''.join(random.choices(string.digits, k=4))
            if not Member.objects.filter(agent_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.agent_code:
            self.agent_code = self.generate_agent_code()
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Monitor(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_login = models.DateTimeField(blank=True, null=True)  # Add this field

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    @property
    def is_authenticated(self):
        return True

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
