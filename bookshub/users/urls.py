from django.conf.urls import patterns

from . import views

urlpatterns = patterns(
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
        views.SingupAPIView.as_view()
    ),
    (
        r'auth/change_password/$',
        views.ChangePasswordAPIView.as_view()
    )
)
