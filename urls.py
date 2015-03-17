from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'infolog-upload.views.index'),
)
