# Generated by Django 5.0.3 on 2024-05-28 18:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0017_rename_content_forummessage_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbotdata',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatbot_data', to='myapi.flow'),
        ),
        migrations.AlterField(
            model_name='flow',
            name='scenery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flows', to='myapi.scenery'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='myapi.flow'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to=settings.AUTH_USER_MODEL),
        ),
    ]
