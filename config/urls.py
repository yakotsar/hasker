from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from hasker.views import index, AskView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ask/', AskView.as_view()),
    path('', index),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

