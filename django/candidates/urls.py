from django.conf.urls import url

from candidates import views

urlpatterns = [
    url(r'^candidates/$', views.candidates),
    url(r'^candidates/(?P<pk>[0-9]+)/$', views.candidate_detail),
]