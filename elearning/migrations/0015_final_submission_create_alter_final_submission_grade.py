# Generated by Django 4.0.3 on 2022-05-25 15:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0014_alter_final_submission_final_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='final_submission',
            name='create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='final_submission',
            name='grade',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
