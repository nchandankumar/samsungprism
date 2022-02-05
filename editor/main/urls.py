from django.urls import path
from . import views

app_name = "main"   


urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('mobile/', views.mobile, name='mobile'),
    path('category/<str:mid>/', views.category, name='category'),
    path('viewimage/<str:mid>/<str:cid>/',views.viewCategoryImage,name='viewimage'),
    path('editor/<str:mid>/<str:cid>/',views.editor,name='editor'),
    path('photocrop/<str:mid>/<str:cid>/',views.photocrop,name='photocrop'),
    path('report/',views.report,name='report')
]