# Generated by Django 3.0.7 on 2020-06-17 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='exchange',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]