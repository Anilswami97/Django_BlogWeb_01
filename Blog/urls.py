from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogHome, name='BlogHome'),
    # API to post a comment.
    path('postComment/', views.postComment, name="BlogComment"),
    path('<str:slug>/', views.blogPost, name='blogPost'),

]
