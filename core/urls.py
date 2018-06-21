from django.urls import path, include
from django.conf.urls import url
from core import views
from django.contrib.auth.views import login,logout
from .forms import LoginForm

urlpatterns = [
    path('', views.topView, name='top'),
    path('plan/<uuid:planId>', views.planView, name='plan'),
    path('plan/<uuid:planId>/<uuid:mobId>', views.planMobView, name='planMob'),
    path('plan/<uuid:planId>/addmob',views.planMobAddView, name='planMobAdd'),
    path('plan/edit/<uuid:planDetailId>/<uuid:mobId>/<int:time>', views.planEditView, name='planEdit'),
    path('edit/', views.addView, name='add'),

    url(r'^regist/$', views.regist, name='regist'),
    url(r'^regist_save/$', views.regist_save, name='regist_save'),

    url(r'^login/$', login,
        {'template_name': 'core/login.html', 'authentication_form': LoginForm},
        name='login'),


    url(r'^logout/$', logout,
        {'template_name': 'core/regist.html'},
        name='logout'),
]