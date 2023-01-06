# Generated by Django 4.1.5 on 2023-01-06 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('seller', models.CharField(max_length=1000)),
                ('seller_url', models.CharField(max_length=1000)),
                ('media_condition', models.CharField(max_length=100)),
                ('sleeve_condition', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('shipping', models.FloatField()),
                ('currency', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=100)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
