# Generated by Django 2.2.28 on 2024-11-16 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personnage',
            fields=[
                ('id_personnage', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('etat', models.CharField(choices=[('Fatigué', 'Fatigué'), ('Rassasié', 'Rassasié'), ('Entraîné', 'Entraîné'), ('Stratégique', 'Stratégique'), ('Prêt', 'Prêt')], max_length=20)),
                ('type_personnage', models.CharField(max_length=20)),
                ('photo', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameModel(
            old_name='Equipement',
            new_name='Lieu',
        ),
        migrations.DeleteModel(
            name='Creature',
        ),
        migrations.AddField(
            model_name='personnage',
            name='lieu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Lieu'),
        ),
    ]