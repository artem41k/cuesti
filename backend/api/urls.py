from rest_framework.routers import SimpleRouter
from django.urls import path

from api import views


router = SimpleRouter(trailing_slash=False)


router.register(
    'manage/forms', views.forms.ManageFormViewSet, basename='forms')


urlpatterns = [
    path('token/refresh', views.auth.CustomTokenRefreshView.as_view()),
    path('token', views.auth.CustomTokenObtainPairView.as_view()),

    path('register', views.users.CreateUserView.as_view()),
    path('profile', views.users.ProfileView.as_view()),

    path('forms/<str:pk>/submit', views.forms.UserSubmitFormView.as_view()),
    path('forms/<str:pk>', views.forms.UserFormView.as_view()),
]

urlpatterns += router.urls
