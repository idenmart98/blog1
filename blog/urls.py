from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>',views.RatingRetrieveUpdateView.as_view(), name='detail'),
    path('register', views.reqister, name='register'),
    path('login', views.loginView, name='login'),
    # path('landing', views.landing, name='landing'), # Daniyar
    path('add_post', views.add_post, name='add_post'), # Arli
    path('user/<int:pk>/', views.user, name='user'), # Bakdoolot
    path('search', views.search, name='search'),
    path('logout/', views.LogoutView.as_view(), name='logout'), 
     # Ainura
    #path('contact', views.contact, name='contact'), # Askat
    #path('404', views.not_found, name='not_found') # Akim
]