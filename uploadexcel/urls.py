from django.conf.urls import url
from . import views

urlpatterns = [
    url('post/img', views.postImg, name = "post_img"),
    url('post/excel', views.postExcel, name = "post_excel"),
    url('register', views.registerPage, name="register"),
    url('login', views.loginPage , name="login"),
    url('logout', views.logoutUser , name="logout"),
    url('', views.home, name="home"),
] 