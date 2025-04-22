from django.contrib import admin
from .models import Hotel, Room, Clients, Reservations, Reviews_and_ratings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ClientsInline(admin.StackedInline):
    model = Clients
    can_delete = False
    verbose_name_plural = 'Дополнительная информация'

class CustomUserAdmin(UserAdmin):
    inlines = (ClientsInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Clients)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Reservations)
admin.site.register(Reviews_and_ratings)



