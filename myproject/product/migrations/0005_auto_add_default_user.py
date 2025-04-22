from django.db import migrations
from django.contrib.auth.models import User

def set_default_user(apps, schema_editor):
    Clients = apps.get_model('product', 'Clients')
    default_user = User.objects.first()
    for client in Clients.objects.filter(user__isnull=True):
        client.user = default_user
        client.save()

class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_hotel_price'),
    ]

    operations = [
        migrations.RunPython(set_default_user),
    ]
