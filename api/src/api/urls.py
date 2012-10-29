from django.conf.urls.defaults import *

urlpatterns = patterns( '',
    (r'^v1/', include('src.api.v1.urls')),
)

