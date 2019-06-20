from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('tagsData/', views.viewTagsData, name='tagData'),
    path('tagsLoc/', views.viewliveLoc, name='liveLoc'),
    path('layoutSelector/', views.viewLayoutSelector, name='layoutSelec'),
    path('nodeSelector/', views.viewNodeSelector, name='nodeSelec'),
    path('tagsLocData/', views.getLocData),
]
