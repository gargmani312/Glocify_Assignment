# Generated by Django 3.1.5 on 2021-01-18 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=256, unique=True)),
                ('Name', models.CharField(max_length=64, null=True)),
            ],
        ),
    ]
