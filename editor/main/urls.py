from django.urls import path
from . import views

app_name = "main"   


urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('mobile/', views.mobile, name='mobile'),
    path('category/<str:mid>/', views.category, name='category'),
    path('viewimage/<str:mid>/<str:cid>/',views.viewCategoryImage,name='viewimage'),
    path('editor/<str:mid>/<str:cid>/',views.editor,name='editor'),
    path('cropedimages/<str:mid>/<str:cid>/',views.cropedimages,name='cropedimages'),
    path('photocrop/<str:mid>/<str:cid>/',views.photocrop,name='photocrop'),
    path('photohighlight/<str:mid>/<str:cid>/',views.photoHighlight,name='photohighlight'),
    path('photocropsave/<str:mid>/<str:cid>/',views.photocropsave,name='photocropsave'),
    path('report/<str:mid>/',views.report,name='report')
]