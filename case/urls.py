from django.urls import path
from .views import Profile, SiteConstructor, LiveDrop, DetailCase, DropItem, SellItem

urlpatterns = [
    path('api/v1/siteconstructor',SiteConstructor.as_view()),
    path('api/v1/livedrop',LiveDrop.as_view()),
    path('api/v1/casedetail/<slug>',DetailCase.as_view()),
    path("api/v1/drop/<slug>",DropItem.as_view()),
    path("api/v1/sell/<pk>",SellItem.as_view(),name="sell"),
    path("api/v1/profile/<slug>",Profile.as_view()),
]