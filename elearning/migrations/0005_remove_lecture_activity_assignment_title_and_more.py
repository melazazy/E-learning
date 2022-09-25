# Generated by Django 4.0.3 on 2022-04-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0004_lecture_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='activity',
        ),
        migrations.AddField(
            model_name='assignment',
            name='title',
            field=models.TextField(default='Assignment', max_length=100),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='lecture_id',
            field=models.ManyToManyField(related_name='lecture_assignment', to='elearning.lecture'),
        ),
        migrations.AlterField(
            model_name='lessonstatus',
            name='lecture_id',
            field=models.ManyToManyField(blank=True, related_name='lecturestate', to='elearning.lecture'),
        ),
        migrations.AlterField(
            model_name='lessonstatus',
            name='lesson_id',
            field=models.ManyToManyField(blank=True, related_name='lessonstate', to='elearning.lesson'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='lecture_id',
            field=models.ManyToManyField(blank=True, related_name='asks', to='elearning.lecture'),
        ),
    ]
