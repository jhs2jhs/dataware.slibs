from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^hello', 'libauth.views.hello'),

)
