
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from smsf.views import DocumentsViewSet, StaffMemberViewSet, \
    SMSFMemberViewSet, SignUpViewSet

router = routers.DefaultRouter()
router.register(r'staff_member', StaffMemberViewSet)
router.register(r'smsf_member', SMSFMemberViewSet)
router.register(r'documents', DocumentsViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpViewSet.as_view(), name='signup'),
    path('signup/<str:uuid>/', SignUpViewSet.as_view(), name='signup'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]