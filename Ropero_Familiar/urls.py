from django.contrib import admin
from django.urls import path
from donaciones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recibir_donacion/', views.receive_donation, name='receive_donation'),
    path('recibir_donacion/<int:id>/', views.items_donation, name='items_donation'),
    path('recibir_donacion/<int:id>/resumen', views.resume_donation, name='resume_donation'),
    path('recibir_donacion/<int:id>/resumen/finalizar', views.finish_donation, name='finish_donation'),
    path('eliminar_donacion/<int:id>/', views.delete_donation, name='delete_donation'),
    path('home/',views.home, name='home'),
    path('registrar_referente_f/',views.register_referring_f, name="register_referring_f"),
    path('registrar_referente_f/<int:id>/',views.register_referring, name="register_referring"),
    path('busqueda_referente/',views.referring_search, name="referring_search"),
    path('referente/<int:id>/',views.referring_profile, name="referring_profile"),
    path('referente/<int:id>/editar',views.edit_referring,name="edit_referring"),
    path('referente/<int:id>/familiares/',views.referring_relatives, name="referring_relatives"),
    path('referente/familiares/perfil_familiar/<int:id>/',views.relative_profile,name='relative_profile'),
    path('referente/<int:id>/familiares/registrar_familiar/',views.register_family, name='register_family'),
    path('cargar_tipos_donacion/',views.load_types_donation, name="load_types_donation"),
    path('cargar_tipos_productos/',views.load_types_products, name ="load_types_products"),
    path('clasificar_productos/',views.sort_products, name ="sort_products"),
    path('adm/agregar_barrio/',views.add_neigh, name="add_neigh"),
    path('login/', views.login, name='login'),
    path('logout/',views.logout, name = 'logout'),
]