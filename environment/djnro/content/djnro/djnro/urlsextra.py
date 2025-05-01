from django.urls import include, path
import edumanage.viewsextra

urlpatterns = [
    path('icingaconf/', edumanage.viewsextra.icingaconf, name="icingaconf"),
    path('radsecproxyconf/', edumanage.viewsextra.radsecproxyconf, name="radsecproxyconf"),
    path('', include('djnro.urls')),
]
