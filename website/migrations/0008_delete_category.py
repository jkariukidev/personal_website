# Generated by Django 4.0.2 on 2022-03-16 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_alter_category_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
    ]
