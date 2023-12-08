# Generated by Django 4.2.7 on 2023-12-08 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginsession',
            name='session',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='default_id', max_length=255, unique=True),
        ),
    ]
