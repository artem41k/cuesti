from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views


router = SimpleRouter(trailing_slash=False)


router.register('manage/forms', views.ManageFormViewSet, basename='forms')


urlpatterns = [
    path('token/refresh', views.CustomTokenRefreshView.as_view()),
    path('token', views.CustomTokenObtainPairView.as_view()),

    path('register', views.CreateUserView.as_view()),
    path('profile', views.ProfileView.as_view()),

    path('forms/<str:pk>/submit', views.UserSubmitFormView.as_view()),
    path('forms/<str:pk>', views.UserFormView.as_view()),
]

urlpatterns += router.urls
