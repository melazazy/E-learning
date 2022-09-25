# Generated by Django 4.0.3 on 2022-05-23 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0011_alter_assignment_submission_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='final_project',
            name='image1_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='final_project',
            name='image2_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='final_project',
            name='video1_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='final_project',
            name='video2_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='assignment_submission',
            name='grade',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
