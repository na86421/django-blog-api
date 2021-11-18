from django.urls import path

from .views import SignUpView, SignInView, UserView

urlpatterns = [
    path('<int:pk>/', UserView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('signin/', SignInView.as_view()),
]
