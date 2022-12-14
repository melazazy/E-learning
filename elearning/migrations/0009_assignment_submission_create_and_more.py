# Generated by Django 4.0.3 on 2022-05-21 02:56

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0008_alter_final_project_title_alter_lessonstatus_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment_submission',
            name='create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment_submission',
            name='answer',
            field=models.URLField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='assignment_submission',
            name='assignment_id',
            field=models.ManyToManyField(related_name='answers', to='elearning.assignment'),
        ),
        migrations.AlterField(
            model_name='assignment_submission',
            name='grade',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='assignment_submission',
            name='user_id',
            field=models.ManyToManyField(related_name='assigns', to=settings.AUTH_USER_MODEL),
        ),
    ]
