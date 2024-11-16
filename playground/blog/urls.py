from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('personnage/<str:id_personnage>/', views.personnage_detail, name='personnage_detail'),
    path('personnage/<str:id_personnage>/?<str:message>', views.personnage_detail, name='personnage_detail_mes'),
]