# Generated by Django 4.0.3 on 2022-05-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0018_remove_grade_course_id_grade_final_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='course_id',
            field=models.ManyToManyField(related_name='graduat', to='elearning.course'),
        ),
    ]
