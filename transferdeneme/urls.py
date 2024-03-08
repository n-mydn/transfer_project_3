"""
URL configuration for transferdeneme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from transfer import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("set_language/<str:language>", views.set_language, name="set-language"),
    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
]

urlpatterns += i18n_patterns(
    path('django_admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('antalya',views.antalya,name="antalya"),
    path('alanya',views.alanya,name="alanya"),
    path('side',views.side,name="side"),
    path('about',views.about,name="about"),
    path('services',views.services,name="services"),
    path('vip_transfer_with_driver',views.vip_transfer_with_driver,name="vip_transfer_with_driver"),
    path('shuttle_transfer',views.shuttle_transfer,name="shuttle_transfer"),
    path('gallery',views.gallery,name="gallery"),
    path('blog',views.blog,name="blog"),
    path('blog_detail/<int:id>',views.blog_detail,name="blog_detail"),
    path('carcall/<int:id>',views.carcall,name="carcall"),
    path('reservation/<int:transfer_id>/<int:car_id>/',views.reservation,name="reservation"),
    path('reservation_detail/<int:id>',views.reservation_detail,name="reservation_detail"),
    path('reservation_query',views.reservation_query,name="reservation_query"),
    path('deneme/<int:transfer_id>/<int:car_id>/',views.deneme,name="deneme"),
    path('admin',views.admin,name="admin"),
    path('admin_about',views.admin_about,name="admin_about"),
    path('admin_services',views.admin_services,name="admin_services"),
    path('admin_index',views.admin_index,name="admin_index"),
    path('admin_reservation_process',views.admin_reservation_process,name="admin_reservation_process"),
    path('admin_reservation_certified',views.admin_reservation_certified,name="admin_reservation_certified"),
    path('admin_reservation_deprecated',views.admin_reservation_deprecated,name="admin_reservation_deprecated"),
    path('admin_reservation_detail/<int:id>',views.admin_reservation_detail,name="admin_reservation_detail"),
    path('admin_price_extras',views.admin_price_extras,name="admin_price_extras"),
    path('admin_price_cars',views.admin_price_cars,name="admin_price_cars"),
    path('admin_cars_add',views.admin_cars_add,name="admin_cars_add"),
    path('admin_car_delete/<int:id>',views.admin_car_delete,name="admin_car_delete"),
    path('admin_blog',views.admin_blog,name="admin_blog"),
    path('admin_blog_detail/<int:id>',views.admin_blog_detail,name="admin_blog_detail"),
    path('admin_blog_delete/<int:id>',views.admin_blog_delete,name="admin_blog_delete"),
    path('admin_gallery',views.admin_gallery,name="admin_gallery"),
    path('logout',views.logout,name="logout"),
    prefix_default_language=False,
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
     path("set_language/<str:language>", views.set_language, name="set-language"),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""