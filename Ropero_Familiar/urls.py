from django.contrib import admin
from django.urls import path
from donaciones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recibir_donacion/', views.receive_donation, name='receive_donation'),
    path('recibir_donacion/<int:id>/', views.items_donation, name='items_donation'),
    path('registrar_familia/',views.register_family, name='register_family'),
    path('home/',views.home, name='home'),
    path('registrar_referente_f/<int:id>',views.register_referring, name="register_referring"),
    path('registrar_referente_f/',views.register_referring_f, name="register_referring_f"),
]
