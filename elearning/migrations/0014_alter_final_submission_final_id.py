# Generated by Django 4.0.3 on 2022-05-25 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0013_alter_final_submission_final_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='final_submission',
            name='final_id',
            field=models.ManyToManyField(related_name='submission', to='elearning.final_project'),
        ),
    ]