# Generated by Django 4.0.3 on 2022-04-21 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0005_remove_lecture_activity_assignment_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='image',
            field=models.URLField(blank=True, max_length=250),
        ),
    ]