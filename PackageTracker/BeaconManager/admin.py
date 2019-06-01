from django.contrib import admin
from BeaconManager.models import Tag
# Register your models here.

#admin.site.register(Tag)

#Register the admin class for Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagID', 'status')
    #list_filter = ('status')