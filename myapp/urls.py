from django.contrib import admin
from django.urls import path,include
from myapp import views

urlpatterns = [
   
    path("",views.index),
  #  path("profile/",views.profile),
    path("setting/",views.setting,name='setting'),
    path("signin/",views.signin,name='signin'),
    path("upload/",views.upload,name='upload'),
    path("likepost/",views.likepost),
    path("profile/<str:pk>/",views.profile),
    path("signup/",views.signup,name='signup'),
    path("userlogout/",views.userlogout),
    path("follow/",views.follow),
    path("search/",views.search,name='search'),
    path("delete/<int:id>/",views.delete,name='delete'),
]
