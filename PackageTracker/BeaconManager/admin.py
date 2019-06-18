from django.contrib import admin
from BeaconManager.models import Tag, Node, Layout
# Register your models here.

#admin.site.register(Tag)

#Register the admin class for Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagID', 'status')
    #list_filter = ('status')

#Register the admin class for Node model
@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('node_id', 'topic', 'layout', 'location')
    #list_filter = ('layout')


class NodesInline(admin.TabularInline):
    model = Node

#Register the admin class for Layout model
@admin.register(Layout)
class LayoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'length', 'width')
    #inlines = [NodesInline]