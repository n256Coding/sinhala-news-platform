# Generated by Django 5.0.6 on 2024-06-22 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('heading', models.TextField()),
                ('category', models.CharField(max_length=50)),
                ('link_to_source', models.TextField()),
            ],
        ),
    ]