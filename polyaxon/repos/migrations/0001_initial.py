# Generated by Django 2.0.3 on 2018-04-12 14:00

from django.db import migrations, models
import django.db.models.deletion
import repos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('commit', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExternalRepo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('git_url', models.URLField()),
                ('is_public', models.BooleanField(default=True, help_text='If repo is public or private.')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_repos', to='projects.Project')),
            ],
            bases=(models.Model, repos.models.RepoMixin),
        ),
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=True, help_text='If repo is public or private.')),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='repo', to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, repos.models.RepoMixin),
        ),
        migrations.AddField(
            model_name='codereference',
            name='external_repo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='references', to='repos.ExternalRepo'),
        ),
        migrations.AddField(
            model_name='codereference',
            name='repo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='references', to='repos.Repo'),
        ),
        migrations.AlterUniqueTogether(
            name='externalrepo',
            unique_together={('project', 'git_url')},
        ),
    ]
