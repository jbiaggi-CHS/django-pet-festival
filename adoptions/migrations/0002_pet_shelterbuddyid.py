# Generated by Django 5.0.4 on 2024-05-03 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adoptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='shelterbuddyId',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]