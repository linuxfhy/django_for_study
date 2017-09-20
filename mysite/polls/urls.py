
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^[0-9]+/flow/$', views.myflow, name='myflow'),
    url(r'^[0-9]+/flow/(?P<model_id>[0-9]+)/detail/$', views.myflowdetail, name='flowdetail'),
    url(r'^[0-9]+/flow/index$', views.NameModelView.as_view(), name='myflowindex'),
    url(r'^[0-9]+/flow/tmp$', views.myflowprocess, name='myflowprocess'),
	url(r'^[0-9]+/flow/regist$', views.flowregist, name='flowregist'),
	url(r'^[0-9]+/flow/login$', views.flowlogin, name='flowlogin'),
]
