# Generated by Django 5.0.6 on 2024-06-03 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0010_alter_relationship_requests_to_childrens_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='requests_to_childrens',
            field=models.ManyToManyField(related_name='request_to_relation_childrens', to='mysite.profile'),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='requests_to_parents',
            field=models.ManyToManyField(related_name='request_to_relation_parents', to='mysite.profile'),
        ),
    ]
