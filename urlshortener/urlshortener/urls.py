from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # if the URL pattern match /admin/ then open up admin panel

    url(r'', include('shortenersite.urls')),
    # if anything rather then /admin/ then it will look for shortenersite/urls
]