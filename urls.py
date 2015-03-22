from django.conf.urls import patterns, include, url
from jsonrpc import jsonrpc_site

import views

urlpatterns = patterns('',
                       url(r'^$', 'infolog_upload.views.index'),
                       url(r'^show/(?P<infologid>[\d-]+)/$', 'infolog_upload.views.infolog_view'),
                       url(r'^not_allowed/(?P<uploader>[\w\ .:()\[\]-]+)/$', 'infolog_upload.views.not_allowed'),
                       url(r'^upload/$', 'infolog_upload.views.upload_html'),
                       url(r'^json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
                       url(r'^json/browse/$', 'jsonrpc.views.browse', name='jsonrpc_browser'),
                       )
