# Generated by Django 5.0.6 on 2024-05-29 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_alter_comfortdefinition_ap_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comfortdefinition',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='devicedetail',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usagedefinition',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]