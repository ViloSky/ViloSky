# Generated by Django 3.1.4 on 2021-03-10 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ViloSkyApp', '0006_auto_20210127_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadioButtonsAdminInput',
            fields=[
                ('admin_input', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ViloSkyApp.admininput')),
                ('choices', models.JSONField()),
            ],
            bases=('ViloSkyApp.admininput',),
        ),
        migrations.AlterField(
            model_name='admininput',
            name='input_type',
            field=models.CharField(choices=[('DROPDOWN', 'Dropdown'), ('TEXT', 'Text'), ('TEXTAREA', 'Textarea'), ('CHECKBOX', 'Checkbox'), ('RADIOBUTTONS', 'Radiobuttons')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='employment_status',
            field=models.CharField(blank=True, choices=[('Unemployed/Volunteer', 'Unemployed Or Volunteer'), ('Employed', 'Employed'), ('Self-Employed', 'Selfemployed'), ('Career Break', 'Career Break'), ('Retired', 'Retired')], max_length=255),
        ),
    ]
