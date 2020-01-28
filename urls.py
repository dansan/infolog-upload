import jsonrpc.views
from django.conf.urls import url
from jsonrpc import jsonrpc_site

from .views import (
    index,
    infolog_view,
    modal_manage_tags,
    modal_manage_tags_add,
    modal_manage_tags_rm,
    not_allowed,
    upload_html,
)

urlpatterns = [url(r'^$', index, name='infolog_upload/index'),
               url(r'^show/(?P<infologid>[\d-]+)/$', infolog_view, name='infolog_upload/show'),
               url(r'^not_allowed/(?P<uploader>[\w\ .:()\[\]-]+)/$', not_allowed, name='infolog_upload/not_allowed'),
               url(r'^upload/$', upload_html, name='infolog_upload/upload_html'),
               url(r'^json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
               url(r'^json/browse/$', jsonrpc.views.browse, name='jsonrpc_browser'),
               url(r'^modal_manage_tags/(?P<infologid>[\d-]+)/$', modal_manage_tags,
                   name='infolog_upload/modal_manage_tags'),
               url(r'^modal_manage_tags_rm/(?P<infologid>[\d-]+)/(?P<tagid>[\d-]+)/$',
                   modal_manage_tags_rm,
                   name='infolog_upload/modal_manage_tags_rm'),
               url(r'^modal_manage_tags_add/(?P<infologid>[\d-]+)/(?P<tagid>[\d-]+)/$',
                   modal_manage_tags_add,
                   name='infolog_upload/modal_manage_tags_add'),
               ]
