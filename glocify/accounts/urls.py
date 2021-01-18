from django.urls import path

from .views import (
    SignUpView,
    LoginView,
    LogOutView,
    ContactMe
)


urlpatterns = [
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup',
    ),
    path('login/', 
        LoginView.as_view(),
        name='login_view'
    ),
    path('logout/', 
        LogOutView.as_view()
    ),
    path('contactme',
        ContactMe.as_view()
    )
]
