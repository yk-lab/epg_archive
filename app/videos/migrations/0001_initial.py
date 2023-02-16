# Generated by Django 4.1.7 on 2023-02-14 15:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=512, verbose_name='title')),
                ('description', models.TextField(default='', verbose_name='description')),
                ('extended', models.TextField(default='', verbose_name='extended')),
                ('genre1', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='genre1')),
                ('sub_genre1', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='sub genre1')),
                ('genre2', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='genre2')),
                ('sub_genre2', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='sub genre2')),
                ('genre3', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='genre3')),
                ('sub_genre3', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='sub genre3')),
                ('video_type', models.CharField(max_length=50, verbose_name='video type')),
                ('video_size', models.PositiveBigIntegerField(verbose_name='video size')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
            },
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.PositiveBigIntegerField(verbose_name='timestamp')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video', verbose_name='Video')),
            ],
            options={
                'verbose_name': 'thumbnail',
                'verbose_name_plural': 'thumbnails',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Channel ID')),
                ('program_id', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Program ID')),
                ('start_at', models.DateTimeField(blank=True, null=True, verbose_name='start at')),
                ('end_at', models.DateTimeField(blank=True, null=True, verbose_name='end at')),
                ('video', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
            options={
                'verbose_name': 'program',
                'verbose_name_plural': 'programs',
            },
        ),
    ]