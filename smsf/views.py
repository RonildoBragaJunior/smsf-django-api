from smsf.mailgun import send_account_activation
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework import filters
from rest_framework import views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from smsf.models import Documents, StaffMember, SMSFMember
from smsf.serializers import DocumentsSerializer, StaffMemberSerializer, SMSFMemberSerializer, UserSerializer, TokenSerializer

class SignUpViewSet(views.APIView):
    def post(self, request):
        serializer = SMSFMemberSerializer(data=request.data)

        if serializer.is_valid():
            try:
                User.objects.get(username=request.data['username'])
                return Response('This email {0} has been taken'.format(request.data['username']), status=status.HTTP_403_FORBIDDEN)
            except User.DoesNotExist:
                instance = serializer.save()
                send_account_activation(instance.user.email)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({serializer.error_messages}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, uuid):
        smsf_member = SMSFMember.objects.get(uuid=uuid)
        serializer = SMSFMemberSerializer(smsf_member, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({serializer.error_messages})


class TokenViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StaffMemberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer

class SMSFMemberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = SMSFMember.objects.all()
    serializer_class = SMSFMemberSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('tax_file_number', 'occupation', 'employer', 'mothers_maiden_name', )

class DocumentsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer