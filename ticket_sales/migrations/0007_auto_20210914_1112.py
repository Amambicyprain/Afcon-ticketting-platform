# Generated by Django 3.2.3 on 2021-09-14 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_sales', '0006_auto_20210913_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='match_image',
        ),
        migrations.RemoveField(
            model_name='match',
            name='match_name',
        ),
    ]