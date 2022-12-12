# Generated by Django 4.0.5 on 2022-10-25 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('isabuhaywebapp', '0002_promooptions_user_uploads_payments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='promo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='isabuhaywebapp.promooptions'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
