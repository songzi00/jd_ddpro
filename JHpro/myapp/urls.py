from django.urls import path
from myapp import views
app_name = '[myapp]'
urlpatterns = [
    path('',views.index,name='index'),
    path('^seach/$',views.seach,name='seach'),
    path('detail/(?P<id>\d+)$',views.detail,name='detail'),
]