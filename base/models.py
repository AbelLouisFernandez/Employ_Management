from django.db import models
from django.contrib.auth.models import User
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Employee(models.Model):
    name = models.CharField(max_length=100)
    availability = models.BooleanField(default=False)
    amount_of_work = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill)
    email=models.EmailField(null=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)
    skills_needed = models.ManyToManyField(Skill)
    deadline = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    task_link=models.CharField(max_length=1000,default=None,null=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)



