from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Employee(models.Model):
    name = models.CharField(max_length=100)
    availability = models.BooleanField(default=False)
    amount_of_work = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.name


class Work(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)
    skills_needed = models.ManyToManyField(Skill)
    deadline = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    


