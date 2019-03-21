# Generated by Django 2.1.7 on 2019-03-19 23:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='InvestmentStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SFund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SMSFMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('annual_income', models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True)),
                ('mothers_maiden_name', models.CharField(max_length=20, unique=True)),
                ('tax_file_number', models.CharField(max_length=20, unique=True)),
                ('Address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='smsf.Address')),
            ],
        ),
        migrations.CreateModel(
            name='SMSFund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True)),
                ('documents', models.ManyToManyField(to='smsf.Documents')),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='staffmember',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='smsf.UserProfile'),
        ),
        migrations.AddField(
            model_name='smsfmember',
            name='contact_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='smsf.StaffMember'),
        ),
        migrations.AddField(
            model_name='smsfmember',
            name='documents',
            field=models.ManyToManyField(to='smsf.Documents'),
        ),
        migrations.AddField(
            model_name='smsfmember',
            name='smsf_fund',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='smsf.SMSFund'),
        ),
        migrations.AddField(
            model_name='smsfmember',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='smsf.UserProfile'),
        ),
        migrations.AddField(
            model_name='sfund',
            name='smsf_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smsf.SMSFMember'),
        ),
        migrations.AddField(
            model_name='investmentstrategy',
            name='smsf_fund',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smsf.SMSFund'),
        ),
    ]