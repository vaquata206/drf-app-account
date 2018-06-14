from django.conf.urls import url
from .views import RegisterAPIView, UserLoginAPIView

urlpatterns = [
    url('register/', RegisterAPIView.as_view()),
    url('login/', UserLoginAPIView.as_view())
]
