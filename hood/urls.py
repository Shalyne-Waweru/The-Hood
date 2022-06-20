from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),  
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    # path('account/', include('django.contrib.auth.urls')),
    path('all-hoods/', views.hoodsView, name='hood'),
    path('new-hood/', views.newHood, name='new-hood'),
    path('profile/', views.profile, name='profile'),
    path('profile/<username>/edit/', views.edit_profile, name='edit-profile'),
    path('join_hood/', views.join_hood, name='join-hood'),
    path('leave_hood/<id>', views.leave_hood, name='leave-hood'),
    path('add_amenity/<hood_id>', views.add_amenity, name='new amenity'),
    path('<hood_id>/new-post', views.create_post, name='post'),
    path('<hood_id>/members', views.hoodMembership, name='members'),
    path('search/', views.search_business, name='search'),
]