# Generated by Django 3.0.7 on 2020-07-12 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20200712_0735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='user',
        ),
        migrations.AddField(
            model_name='item',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Account'),
            preserve_default=False,
        ),
    ]
