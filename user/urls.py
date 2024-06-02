from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserCreateView, UserEditView, PasswordResetView, SetPasswordView, ActivateAccountView, \
    GoogleLoginView, FacebookLoginView, GetUserIdView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/edit/<int:pk>/', UserEditView.as_view(), name='user-edit'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('set-password/<uidb64>/<token>/', SetPasswordView.as_view(), name='set-password'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

    # path('dj-rest-auth/facebook/', )),
    path('dj-rest-auth/google/', GoogleLoginView.as_view({"post": "login_or_signup"})),
    path('dj-rest-auth/facebook/', FacebookLoginView.as_view({"post": "login_or_signup"})),

    path('user-id/', GetUserIdView.as_view(), name='get-user-id'),
    # path('accounts/', include('allauth.urls')),
    # path('dj-rest-auth/jwt/create/', JWTCookieAuthentication.as_view(), name='jwt-create'),
]
