# Generated by Django 2.2.3 on 2023-09-11 11:17

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_developer', models.BooleanField(default=False)),
                ('is_teamlead', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=1000, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('attachments', models.FileField(max_length=1000, null=True, upload_to='')),
                ('status', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DevProjectUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.CharField(max_length=1000, null=True)),
                ('attachments', models.FileField(max_length=1000, null=True, upload_to='')),
                ('status', models.CharField(max_length=100, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.ProjectAssignment')),
            ],
        ),
        migrations.CreateModel(
            name='AppStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, null=True)),
                ('projectApp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.DevProjectUpdate')),
            ],
        ),
        migrations.CreateModel(
            name='Teamlead',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('developer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Developer')),
            ],
        ),
        migrations.AddField(
            model_name='projectassignment',
            name='by_admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Admin'),
        ),
        migrations.AddField(
            model_name='projectassignment',
            name='developers',
            field=models.ManyToManyField(blank=True, related_name='assigned_projects', to='company.Developer'),
        ),
        migrations.AddField(
            model_name='projectassignment',
            name='to_lead',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='company.Teamlead'),
        ),
        migrations.CreateModel(
            name='LeadProjectUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.CharField(max_length=1000, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('attachments', models.FileField(max_length=1000, null=True, upload_to='')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.ProjectAssignment')),
                ('to_admin', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='company.Admin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Teamlead')),
            ],
        ),
        migrations.AddField(
            model_name='devprojectupdate',
            name='to_teamlead',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='company.Teamlead'),
        ),
        migrations.AddField(
            model_name='devprojectupdate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Developer'),
        ),
        migrations.AddField(
            model_name='admin',
            name='teamlead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Teamlead'),
        ),
    ]
