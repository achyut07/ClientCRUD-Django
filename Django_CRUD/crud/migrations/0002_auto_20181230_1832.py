# Generated by Django 2.1.4 on 2018-12-30 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientlist',
            name='company_logo',
            field=models.ImageField(blank=True, default='media/pic_folder/no-image.png', null=True, upload_to='media/pic_folder/'),
        ),
    ]