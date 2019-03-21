from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from smsf.models import Documents
from smsf.serializers import DocumentsSerializer, StaffMemberSerializer


class StaffMemberView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = StaffMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'A new staff has been saved'})
        else:
            return Response({'The data you sent is not valid'})


class DocumentsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer