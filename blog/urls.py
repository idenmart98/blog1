from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>',views.RatingRetrieveUpdateView.as_view(), name='detail'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('add_post', views.NewPostView.as_view(), name='add_post'), 
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('search', views.SearchView.as_view(), name='search'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]