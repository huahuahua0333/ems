"""
URL configuration for ems project.
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from app01.views import depart, user, pretty

urlpatterns = [
    path('admin/', admin.site.urls),

    # 根路径重定向到部门列表
    re_path(r'^$', RedirectView.as_view(url='/depart/list/')),

    # 部门管理
    path('depart/list/', depart.depart_list, name='depart_list'),
    path('depart/add/', depart.depart_add, name='depart_add'),
    path('depart/<int:nid>/edit/', depart.depart_edit, name='depart_edit'),
    path('depart/<int:nid>/delete/', depart.depart_delete, name='depart_delete'),

    # 用户管理
    path('user/list/', user.user_list, name='user_list'),
    path('user/add/', user.user_add, name='user_add'),
    path('user/<int:nid>/edit/', user.user_edit, name='user_edit'),
    path('user/<int:nid>/delete/', user.user_delete, name='user_delete'),

    # 靓号管理
    path('pretty/list/', pretty.pretty_list, name='pretty_list'),
    path('pretty/add/', pretty.pretty_add, name='pretty_add'),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit, name='pretty_edit'),
    path('pretty/<int:nid>/delete/', pretty.pretty_delete, name='pretty_delete'),
]
