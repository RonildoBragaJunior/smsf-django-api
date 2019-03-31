from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from smsf.models import Documents, StaffMember, SMSFMember
from smsf.serializers import DocumentsSerializer, StaffMemberSerializer, SMSFMemberSerializer
from rest_framework.response import Response


class SignUpViewSet(views.APIView):
    def post(self, request):
        serializer = SMSFMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({serializer.error_messages})

    def patch(self, request, uuid):
        smsf_member = SMSFMember.objects.get(uuid=uuid)
        serializer = SMSFMemberSerializer(smsf_member, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({serializer.error_messages})


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