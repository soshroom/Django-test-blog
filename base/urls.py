from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('post/<int:pk>/', views.PostPage),
    path('likePost/', views.likePost),
    path('likeComment/', views.likeComment),
    path('login/', views.loginPage),
    path('register/', views.registerPage),
    path('post/<int:pk>/addComment/', views.addComment),
    path('newPost/', views.newPost)
]
