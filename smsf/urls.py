
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from smsf.views import DocumentsViewSet, StaffMemberView

router = routers.DefaultRouter()
router.register(r'documents', DocumentsViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('staff_member/', StaffMemberView.as_view(), name='staff_member'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]