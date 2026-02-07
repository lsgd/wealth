# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_add_send_daily_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='send_daily_report',
            new_name='send_weekly_report',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='send_weekly_report',
            field=models.BooleanField(default=False, help_text='Send weekly wealth summary email on Mondays'),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='sync_frequency_hours',
        ),
    ]
