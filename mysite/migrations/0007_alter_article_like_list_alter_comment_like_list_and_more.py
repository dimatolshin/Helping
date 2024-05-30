# Generated by Django 5.0.6 on 2024-05-30 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_remove_room_current_users_remove_room_host_article_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='like_list',
            field=models.ManyToManyField(blank=True, related_name='articles_like_list', to='mysite.profile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='like_list',
            field=models.ManyToManyField(blank=True, related_name='comments_like_list', to='mysite.profile'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='current_profiles',
            field=models.ManyToManyField(blank=True, related_name='topics', to='mysite.profile'),
        ),
    ]
