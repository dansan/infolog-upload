from django.conf.urls import url
from jsonrpc import jsonrpc_site
import jsonrpc.views

import infolog_upload.views

urlpatterns = [url(r'^$', infolog_upload.views.index, name='infolog_upload/index'),
               url(r'^show/(?P<infologid>[\d-]+)/$', infolog_upload.views.infolog_view, name='infolog_upload/show'),
               url(r'^not_allowed/(?P<uploader>[\w\ .:()\[\]-]+)/$', infolog_upload.views.not_allowed, name='infolog_upload/not_allowed'),
               url(r'^upload/$', infolog_upload.views.upload_html, name='infolog_upload/upload_html'),
               url(r'^json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
               url(r'^json/browse/$', jsonrpc.views.browse, name='jsonrpc_browser'),
               url(r'^modal_manage_tags/(?P<infologid>[\d-]+)/$', infolog_upload.views.modal_manage_tags,
                   name='infolog_upload/modal_manage_tags'),
               url(r'^modal_manage_tags_rm/(?P<infologid>[\d-]+)/(?P<tagid>[\d-]+)/$',
                   infolog_upload.views.modal_manage_tags_rm,
                   name='infolog_upload/modal_manage_tags_rm'),
               url(r'^modal_manage_tags_add/(?P<infologid>[\d-]+)/(?P<tagid>[\d-]+)/$',
                   infolog_upload.views.modal_manage_tags_add,
                   name='infolog_upload/modal_manage_tags_add'),
               ]
