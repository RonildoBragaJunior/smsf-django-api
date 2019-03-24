# Generated by Django 2.1.7 on 2019-03-24 04:05

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
                ('street_name', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.IntegerField(blank=True, null=True)),
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
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SFund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SMSFMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('annual_income', models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True)),
                ('mothers_maiden_name', models.CharField(blank=True, max_length=20, null=True)),
                ('tax_file_number', models.CharField(blank=True, max_length=20, null=True)),
                ('occupation', models.CharField(blank=True, max_length=20, null=True)),
                ('employer', models.CharField(blank=True, max_length=20, null=True)),
                ('accept_terms', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SMSFund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True)),
                ('documents', models.ManyToManyField(to='smsf.Documents')),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
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
            name='place_of_birth',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='smsf_member_place_of_birth', to='smsf.Address'),
        ),
        migrations.AddField(
            model_name='smsfmember',
            name='place_of_residence',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='smsf_member_place_of_residence', to='smsf.Address'),
        ),
        migrations.AddField(
            model_name='smsfmember',
            name='smsfund',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='smsf_members', to='smsf.SMSFund'),
        ),
        migrations.AddField(
            model_name='smsfmember',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sfund',
            name='smsf_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sfunds', to='smsf.SMSFMember'),
        ),
        migrations.AddField(
            model_name='investmentstrategy',
            name='smsfund',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investment_strategies', to='smsf.SMSFund'),
        ),
    ]
