from django.urls import include, path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('login/', views.signin, name='login'),
    path('signuppage/', views.signup_page, name='signuppage'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<int:id>/', views.details_by_id, name='iddetails'),
    path('userdetails/', views.user_details, name='userdetails'),
    path('accounts/profile/', views.account_profile, name='accountsprofile'),
    path('gitsignup/', views.git_signup, name='gitlogin'),
    path('user/set_password', views.set_password, name='setpassword'),
    path('user/set_password_view', views.set_password_view, name='setpasswordview'),
    path('user/search/', views.search_user, name='searchuser')

]