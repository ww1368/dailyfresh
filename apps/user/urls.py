
from django.urls import path
from apps.user import views
from apps.user.views import RegisterView, ActiveView, LoginView
app_name = 'user'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('active/<str:token>/', ActiveView.as_view(), name='active'),
    path('login/', LoginView.as_view(), name='login'),

]
