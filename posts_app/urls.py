from django.urls import path
from . import views
from .views import CustomLoginView, RegisterPage, PostListView, PostCreateView,user_logout,perfil
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home-page'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('perfil/', perfil, name='perfil'),
    path('logout/', user_logout, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('post/', PostListView.as_view(), name='post-list'),
    path('post-create/', login_required(PostCreateView.as_view()), name='post-create'),
    path('post-update/<int:id>/', views.post_update, name='post-update'),
    path('post-delete/<int:id>/', views.post_delete, name='post-delete'),
]
