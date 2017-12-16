
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<prj_name>[a-zA-Z0-9_]+)/home/$', views.flowprjhome, name='flowprjhome'),
    url(r'^(?P<prj_name>[a-zA-Z0-9_]+)/regist$', views.flowregist, name='flowprjregist'),
    url(r'^(?P<prj_name>[a-zA-Z0-9_]+)/new/$', views.flow_create_question, name='myflow'),
    url(r'^(?P<prj_name>[a-zA-Z0-9_]+)/index/$', views.flowindex, name='myflowindex'),
    url(r'^(?P<prj_name>[a-zA-Z0-9_]+)/cur_user/$', views.flow_index_for_current_user, name='PrjIndexForCurUser'),
    url(r'^(?P<prj_name>[a-zA-Z0-9_]+)/grpauthadmin/$', views.flow_grp_auth_admin, name='flowgrpauthadmin'),
    url(r'^(?P<prj_name>[a-zA-Z0-9_]+)/exportdata$', views.flow_export_excel, name='flowprjexport'),
    url(r'^(?P<prj_name>[a-zA-Z0-9_]+)/(?P<model_id>[0-9]+)/detail/$', views.myflowdetail, name='flowdetail'),
    url(r'^tmp$', views.myflowprocess, name='myflowprocess'),
    url(r'^regist$', views.flowregist, name='flowregist'),
    url(r'^login$', views.flowlogin, name='flowlogin'),
    url(r'^logout$', views.flowlogout, name='flowlogout'),
    url(r'^home$', views.flowhome, name='flowhome')
]
