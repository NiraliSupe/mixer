from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from mixer import views

urlpatterns = [
    url(r'address/$', views.MixerAddress.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)