# Generated by Django 2.0.3 on 2018-04-12 14:00

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import libs.blacklist
import libs.models
import re
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('execute_at', models.DateTimeField(blank=True, help_text='When this instance should be executed. default None which translate to now', null=True)),
                ('timeout', models.PositiveIntegerField(blank=True, help_text='specify how long this instance should be up before timing out in seconds.', null=True)),
                ('trigger_policy', models.CharField(blank=True, choices=[('all_succeeded', 'all_succeeded'), ('all_failed', 'all_failed'), ('all_done', 'all_done'), ('one_succeeded', 'one_succeeded'), ('one_failed', 'one_failed'), ('one_done', 'one_done')], default='all_succeeded', help_text='defines the rule by which dependencies are applied, default is `all_success`.', max_length=16, null=True)),
                ('max_retries', models.PositiveSmallIntegerField(blank=True, help_text='the number of retries that should be performed before failing the operation.', null=True)),
                ('retry_delay', models.PositiveIntegerField(blank=True, default=60, help_text='The delay between retries.', null=True)),
                ('retry_exponential_backoff', models.BooleanField(default=False, help_text='allow progressive longer waits between retries by using exponential backoff algorithm on retry delay.')),
                ('max_retry_delay', models.PositiveIntegerField(blank=True, default=3600, help_text='maximum delay interval between retries.', null=True)),
                ('concurrency', models.PositiveSmallIntegerField(blank=True, help_text='When set, an operation will be able to limit the concurrent runs across execution_dates', null=True)),
                ('run_as_user', models.CharField(blank=True, help_text='unix username to impersonate while running the operation.', max_length=64, null=True)),
                ('config', models.TextField(blank=True, null=True)),
                ('celery_task', models.CharField(help_text='The celery task name to execute.', max_length=128)),
                ('celery_queue', models.CharField(blank=True, help_text='The celery queue name to use for the executing this task. If provided, it will override the queue provided in CELERY_TASK_ROUTES.', max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperationRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('celery_task_context', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='The kwargs required to execute the celery task.', null=True)),
                ('celery_task_id', models.CharField(blank=True, max_length=36)),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='pipelines.Operation')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, libs.models.LastStatusMixin),
        ),
        migrations.CreateModel(
            name='OperationRunStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('message', models.CharField(blank=True, max_length=256, null=True)),
                ('status', models.CharField(blank=True, choices=[('created', 'created'), ('scheduled', 'scheduled'), ('running', 'running'), ('finished', 'finished'), ('stopped', 'stopped'), ('skipped', 'skipped')], default='created', max_length=64, null=True)),
                ('operation_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='pipelines.OperationRun')),
            ],
            options={
                'verbose_name_plural': 'Operation Run Statuses',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('execute_at', models.DateTimeField(blank=True, help_text='When this instance should be executed. default None which translate to now', null=True)),
                ('timeout', models.PositiveIntegerField(blank=True, help_text='specify how long this instance should be up before timing out in seconds.', null=True)),
                ('name', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid'), libs.blacklist.validate_blacklist_name])),
                ('concurrency', models.PositiveSmallIntegerField(blank=True, help_text='If set, it determines the number of operation instances allowed to run concurrently.', null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pipelines', to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PipelineRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='pipelines.Pipeline')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, libs.models.LastStatusMixin),
        ),
        migrations.CreateModel(
            name='PipelineRunStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('message', models.CharField(blank=True, max_length=256, null=True)),
                ('status', models.CharField(blank=True, choices=[('created', 'created'), ('scheduled', 'scheduled'), ('running', 'running'), ('finished', 'finished'), ('stopped', 'stopped'), ('skipped', 'skipped')], default='created', max_length=64, null=True)),
                ('pipeline_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='pipelines.PipelineRun')),
            ],
            options={
                'verbose_name_plural': 'Pipeline Run Statuses',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('frequency', models.CharField(blank=True, help_text="Defines how often to run, this timedelta object gets added to your latest operation instance's execution_date to figure out the next schedule", max_length=64, null=True)),
                ('start_at', models.DateTimeField(blank=True, help_text='When this instance should run, default is None which translate to now.', null=True)),
                ('end_at', models.DateTimeField(blank=True, help_text='When this instance should stop running, default is None which translate to open ended.', null=True)),
                ('depends_on_past', models.BooleanField(default=False, help_text="when set to true, the instances will run sequentially while relying on the previous instances' schedule to succeed.")),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='pipelinerun',
            name='status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pipelines.PipelineRunStatus'),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='schedule',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pipelines.Schedule'),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pipelines', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='operationrun',
            name='pipeline_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation_runs', to='pipelines.PipelineRun'),
        ),
        migrations.AddField(
            model_name='operationrun',
            name='status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pipelines.OperationRunStatus'),
        ),
        migrations.AddField(
            model_name='operationrun',
            name='upstream_runs',
            field=models.ManyToManyField(blank=True, related_name='downstream_runs', to='pipelines.OperationRun'),
        ),
        migrations.AddField(
            model_name='operation',
            name='pipeline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='pipelines.Pipeline'),
        ),
        migrations.AddField(
            model_name='operation',
            name='schedule',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pipelines.Schedule'),
        ),
        migrations.AddField(
            model_name='operation',
            name='upstream_operations',
            field=models.ManyToManyField(blank=True, related_name='downstream_operations', to='pipelines.Operation'),
        ),
    ]
