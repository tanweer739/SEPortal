# Generated by Django 3.0 on 2020-03-17 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reportsick', '0003_auto_20200317_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='report',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='reportsick.Report'),
        ),
    ]
