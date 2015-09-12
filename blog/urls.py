from django.conf.urls import url


urlpatterns = [

    # 함수로 구현된 url 목록
    # url(r'^$', 'blog.views.index', name='index'),
    # url(r'^(?P<uuid>[0-9a-f]{32})/$', 'blog.views.detail', name='detail'),
    # url(r'^(?P<pk>\d+)/$', 'blog.views.detail', name='detail'),
    # url(r'^new/$', 'blog.views.new', name='new'),
    # url(r'^(?P<pk>\d+)/edit/$', 'blog.views.edit', name='edit'),

    # Class Based View(클래스)로 구현된 url 목록
    url(r'^$', 'blog.views_cbv.index', name='index'),
    url(r'^(?P<uuid>[0-9a-f]{32})/$', 'blog.views_cbv.detail', name='detail'),
    url(r'^(?P<pk>\d+)/$', 'blog.views_cbv.detail', name='detail'),
    url(r'^new/$', 'blog.views_cbv.new', name='new'),
    url(r'^(?P<pk>\d+)/edit/$', 'blog.views_cbv.edit', name='edit'),



    url(r'^(?P<pk>\d+)/comments/new/$', 'blog.views.comment_new', name='comment_new'),
    url(r'^(?P<post_pk>\d+)/comments/(?P<pk>\d+)/edit/$', 'blog.views.comment_edit', name='comment_edit'),

    url(r'^(?P<post_pk>\d+)/comments/(?P<pk>\d+)/delete/$', 'blog.views.comment_delete', name='comment_delete'),

    url(r'^image/$', 'blog.views.image', name='image'),
]