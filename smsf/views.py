from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from smsf.models import Documents, StaffMember, SMSFMember
from smsf.serializers import DocumentsSerializer, StaffMemberSerializer, SMSFMemberSerializer


class StaffMemberViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer


class SMSFMemberViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = SMSFMember.objects.all()
    serializer_class = SMSFMemberSerializer


class DocumentsViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer