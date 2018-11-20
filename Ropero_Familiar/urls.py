from django.contrib import admin
from django.urls import path
from donaciones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recibir_donacion/', views.receive_donation, name='receive_donation'),
    path('recibir_donacion/<int:id>/', views.items_donation, name='items_donation'),
    path('recibir_donacion/<int:id>/resumen', views.resume_donation, name='resume_donation'),
    path('recibir_donacion/<int:id>/resumen/finalizar', views.finish_donation, name='finish_donation'),
    path('registrar_familia/',views.register_family, name='register_family'),
    path('home/',views.home, name='home'),
    path('registrar_referente_f/<int:id>',views.register_referring, name="register_referring"),
    path('registrar_referente_f/',views.register_referring_f, name="register_referring_f"),
    path('cargar_tipos_donacion/',views.load_types_donation, name="load_types_donation"),
    path('cargar_tipos_productos/',views.load_types_products, name ="load_types_products"),
    path('clasificar_productos/',views.sort_products, name ="sort_products"),

]
