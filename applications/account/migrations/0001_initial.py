# Generated by Django 4.2.7 on 2023-12-04 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('grade', models.SmallIntegerField()),
                ('classroom', models.SmallIntegerField()),
                ('number', models.SmallIntegerField()),
                ('auth', models.SmallIntegerField()),
                ('password', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='LoginSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=32)),
                ('allot_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
    ]
