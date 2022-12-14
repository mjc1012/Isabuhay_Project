# Generated by Django 4.1.2 on 2022-11-14 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("isabuhaywebapp", "0008_alter_user_uploads"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="date_created",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="date created"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="uploads",
            field=models.IntegerField(default=5, verbose_name="uploads"),
        ),
    ]
