# Generated by Django 5.0.3 on 2024-05-21 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0012_alter_appuser_username_chatbotdata'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='chatbotdata',
            table='training',
        ),
    ]