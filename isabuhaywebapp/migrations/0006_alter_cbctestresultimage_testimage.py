# Generated by Django 4.1.2 on 2022-10-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isabuhaywebapp', '0005_alter_cbctestresultimage_testimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cbctestresultimage',
            name='testImage',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
