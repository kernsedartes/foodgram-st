# Generated by Django 5.2.1 on 2025-05-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name='recipes',
                to='api.tag',
                verbose_name='Теги'),
        ),
    ]
