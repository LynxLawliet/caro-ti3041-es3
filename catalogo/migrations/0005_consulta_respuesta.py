import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0004_consultacliente'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='consultacliente',
            name='respuesta',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='consultacliente',
            name='respondida_en',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='consultacliente',
            name='respondida_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultas_respondidas', to=settings.AUTH_USER_MODEL),
        ),
    ]
