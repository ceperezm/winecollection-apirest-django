from django.contrib import admin

from .models import WineComment, ClientCollectionComment

admin.site.register(WineComment)
admin.site.register(ClientCollectionComment)
