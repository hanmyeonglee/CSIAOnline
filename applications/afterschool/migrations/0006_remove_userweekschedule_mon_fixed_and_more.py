# Generated by Django 4.2.7 on 2023-12-07 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_password'),
        ('afterschool', '0005_alter_classinformation_class_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userweekschedule',
            name='mon_fixed',
        ),
        migrations.RemoveField(
            model_name='userweekschedule',
            name='thr_fixed',
        ),
        migrations.RemoveField(
            model_name='userweekschedule',
            name='tue_fixed',
        ),
        migrations.RemoveField(
            model_name='userweekschedule',
            name='wed_fixed',
        ),
        migrations.AddField(
            model_name='userweekschedule',
            name='participate',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='AfterSchoolUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mon_fixed', models.CharField(max_length=10)),
                ('tue_fixed', models.CharField(max_length=10)),
                ('wed_fixed', models.CharField(max_length=10)),
                ('thr_fixed', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
        migrations.AlterField(
            model_name='userweekschedule',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='afterschool.afterschooluser'),
        ),
    ]
