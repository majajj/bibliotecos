# Generated by Django 3.2.3 on 2021-10-11 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_list_processor', '0003_keywordstosearch'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordstosearch',
            name='keyword_description',
            field=models.CharField(default=None, max_length=255),
        ),
    ]