# Generated by Django 3.0.5 on 2020-04-18 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_oauthcode_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedrepos',
            name='open_issues',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='selectedrepos',
            name='stars',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
