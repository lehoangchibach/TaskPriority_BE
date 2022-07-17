from django.db import models

# Create your models here.


class Users(models.Model):
    userName = models.CharField(unique=True, max_length=30, primary_key=True)
    displayName = models.CharField(max_length=30)
    password = models.CharField(max_length=40)


class Task(models.Model):
    PRIORITY_CHOICES = (
        ('Low', 'low'),
        ('Normal', 'normal'),
        ('High', 'high'),
        ('Doing', 'doing'),
        ('Done', 'done'),
    )
    owner = models.OneToOneField(
        Users,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30)
    summary = models.CharField(max_length=250)
    detail = models.TextField(max_length=500, blank=True)
    deadlineTime = models.TimeField()
    deadlineDate = models.DateField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)


class Tasks(models.Model):
    owner = models.OneToOneField(
        Users,
        on_delete=models.CASCADE
    )
    low = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        limit_choices_to={'priority': 'low'},
        related_name='+',

    )
    normal = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        limit_choices_to={'priority': 'normal'},
        related_name='+',
    )
    high = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        limit_choices_to={'priority': 'high'},
        related_name='+',
    )
    doing = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        limit_choices_to={'priority': 'doing'},
        related_name='+',
    )
    done = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        limit_choices_to={'priority': 'done'},
        related_name='+',
    )