from django.contrib import admin
from .models import ProviderCollection, ClientCollection, Type, ClientCollectionWine, ProviderCollectionWine

# Register your models here.
admin.site.register(ProviderCollection)
admin.site.register(ClientCollection)
admin.site.register(Type)
admin.site.register(ClientCollectionWine)
admin.site.register(ProviderCollectionWine)