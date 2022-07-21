# Generated by Django 4.0.6 on 2022-07-20 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskPriority_BE', '0003_task_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Low Priority'), ('normal', 'Normal Priority'), ('high', 'High Priority'), ('doing', 'Doing'), ('done', 'Done')], max_length=6),
        ),
    ]