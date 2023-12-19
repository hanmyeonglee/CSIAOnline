# Generated by Django 4.2.7 on 2023-12-14 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afterschool', '0013_alter_afterschooluser_mon_fixed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seminarroombook',
            name='room1',
        ),
        migrations.RemoveField(
            model_name='seminarroombook',
            name='room2',
        ),
        migrations.RemoveField(
            model_name='seminarroombook',
            name='room3',
        ),
        migrations.RemoveField(
            model_name='seminarroombook',
            name='room4',
        ),
        migrations.RemoveField(
            model_name='seminarroombook',
            name='room5',
        ),
        migrations.RemoveField(
            model_name='seminarroombook',
            name='room6',
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room1_1',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room1_2',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room1_3',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room2_1',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room2_2',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room2_3',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room3_1',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room3_2',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room3_3',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room4_1',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room4_2',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room4_3',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room5_1',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room5_2',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room5_3',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room6_1',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room6_2',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='seminarroombook',
            name='room6_3',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='seminarroombook',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]