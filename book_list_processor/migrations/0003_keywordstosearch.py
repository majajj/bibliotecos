# Generated by Django 3.2.3 on 2021-10-11 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_list_processor', '0002_rename_pulication_language_books_publication_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordsToSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=255)),
            ],
        ),
    ]