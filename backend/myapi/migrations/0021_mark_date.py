# Generated by Django 5.0.3 on 2024-05-29 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0020_alter_flow_scenery'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default="2024-05-29 15:49:04.423846+02"),
            preserve_default=False,
        ),
    ]