from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from donaciones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('recibir_donacion/', views.receive_donation, name='receive_donation'),
    path('recibir_donacion/<int:id>/', views.items_donation, name='items_donation'),
    path('recibir_donacion/<int:id>/resumen', views.resume_donation, name='resume_donation'),
    path('recibir_donacion/<int:id>/resumen/finalizar', views.finish_donation, name='finish_donation'),
    path('editar_donacion/<int:id>/', views.edit_donation, name='edit_donation'),
    path('eliminar_donacion/', views.delete_donation, name='delete_donation'),
    path('home/', views.home, name='home'),
    # path('registrar_referente_f/', views.register_referring_f, name="register_referring_f"),
    # path('registrar_referente_f/<int:id>/', views.register_referring, name="register_referring"),
    path('registrar_referente/', views.register_referring, name="register_referring"),
    path('busqueda_referente/', views.referring_search, name="referring_search"),
    path('referente/<int:id>/', views.referring_profile, name="referring_profile"),
    path('referente/<int:id>/editar', views.edit_referring, name="edit_referring"),
    path('referente/<int:id>/familiares/', views.referring_relatives, name="referring_relatives"),
    path('referente/familiares/perfil_familiar/<int:id>/', views.relative_profile, name='relative_profile'),
    path('referente/familiares/perfil_familiar/<int:id>/editar', views.edit_family, name='edit_family'),
    path('referente/<int:id>/familiares/registrar_familiar/', views.register_family, name='register_family'),
    path('cargar_tipos_donacion/', views.load_types_donation, name="load_types_donation"),
    path('tipos_productos/', views.load_types_products, name="load_types_products"),
    path('tipos_productos/<int:id>', views.update_price_article, name="update_price_article"),
    path('clasificar_productos/', views.sort_products, name="sort_products"),
    path('clasificar_acondicionar/', views.fix_products, name="fix_products"),
    path('lista_donaciones/', views.list_sort, name="list_sort"),
    path('lista_acondicionar/', views.list_fix, name="list_fix"),
    path('lista_responsable/', views.agregate_responsable, name="agregate_responsable"),
    path('responsable/', views.responsable, name="responsable"),
    path('devolver/<int:id>', views.give_back, name="give_back"),
    path('para_acondicionar/<int:id>/resumen', views.resume_fix, name="resume_fix"),
    path('para_acondicionar/<int:id>', views.carry_out, name="carry_out"),
    path('eliminar_acondicionar/<int:id>/', views.delete_fix, name='delete_fix'),
    path('adm/barrios/', views.neigh, name="neigh"),
    path('adm/barrios/<int:id>', views.edit_neigh, name='edit_neigh'),
    path('adm/barrios/<int:id>/borrar', views.del_neigh, name='del_neigh'),
    path('adm/registrar_usuario/', views.register_user, name="register_user"),
    path('adm/reporte_donaciones/', views.donations_report, name="donations_report"),
    path('adm/reporte_ventas/', views.sales_report, name="sales_report"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ingreso_ropero/', views.closet, name='closet'),
    path('ingreso_ropero/ok/<int:id>/', views.entry_ok, name="entry_ok"),
    path('personas_ropero/', views.peoples_closet, name="peoples_closet"),
    path('personas_ropero/venta/<int:id>/', views.sale, name="sale"),
    path('personas_ropero/venta/<int:id>/detalles', views.sale_detail, name="sale_detail"),
    path('personas_ropero/venta/<int:id>/detalles/resumen/', views.summary_sale, name="summary_sale"),
    path('eliminar_venta/', views.delete_sale, name='delete_sale'),
    path('perfil_usuario/', views.profile_user, name='profile_user'),
    path('creditos/', views.credits, name="credits"),
    path('perfil_usuario/<int:id>/editar', views.profile_user_edit, name='profile_user_edit'),
    path('usuario/<int:id>/cambiar_pass', views.change_password, name='change_password'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
