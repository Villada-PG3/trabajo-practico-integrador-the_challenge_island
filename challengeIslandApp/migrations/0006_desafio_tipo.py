from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challengeIslandApp', '0005_alter_detalleconjunto_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='desafio',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('fisica', 'Física'),
                    ('mental', 'Mental'),
                    ('estrategica', 'Estratégica'),
                ],
                default='estrategica',
                max_length=12,
            ),
        ),
    ]
