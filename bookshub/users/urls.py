from django.conf.urls import patterns
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'users/(?P<user_id>\d+)/reviews', views.UserReviewViewSet)

urlpatterns = router.urls

urlpatterns += patterns(
    # Prefix
    '',
    (
        r'auth/signin/$',
        views.SigninAPIView.as_view()
    ),
    (
        r'autocomplete/users/$',
        views.UserAutoCompleteAPIView.as_view()
    ),
    (
        r'auth/signup/$',
        views.SignupAPIView.as_view()
    ),
    (
        r'auth/change_password/$',
        views.ChangePasswordAPIView.as_view()
    ),
    (
        r'auth/forgot_password/$',
        views.ForgotPasswordAPIView.as_view()
    ),
    (
        r'auth/reset_password/$',
        views.ResetPasswordAPIView.as_view()
    ),
    (
        r'auth/cancel_account/$',
        views.CancelAccountAPIView.as_view()
    ),
    (
        r'auth/settings/$',
        views.UserSettingsAPIView.as_view()
    ),
    (
        r'auth/users/(?P<id>\d+)/profile/$',
        views.UserProfileAPIView.as_view()
    ),
    (
        r'^auth/refresh_token/',
        'rest_framework_jwt.views.refresh_jwt_token'
    ),
    (
        r'auth/subscription/$',
        views.StripeCreateSubscriptionView.as_view()
    ),

)
