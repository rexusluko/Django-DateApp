# Generated by Django 4.2.4 on 2023-08-30 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('date_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name_plural': 'Лайки'},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'Друзья'},
        ),
    ]
