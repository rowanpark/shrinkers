from django.http import Http404  # 아래 표현 방식보다 더 일반적으로 흔하게 사용
# from django.http.response import Http404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from shortener.models import ShortenedUrls
from shortener.urls.serializers import UrlCreateSerializer, UrlListSerializer
from shortener.utils import MsgOk, url_count_changer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ShortenedUrls.objects.all().order_by('-created_at')
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]


class UrlListViewSet(viewsets.ModelViewSet):
    queryset = ShortenedUrls.objects.order_by('-created_at')
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        # POST METHOD
        serializer = UrlCreateSerializer(data=request.data)
        print('serializer:', serializer)
        print('serializer.is_valid():', serializer.is_valid())
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # Detail GET
        queryset = self.get_queryset().filter(pk=pk).first()
        serializer = UrlListSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # PUT METHOD
        pass

    def partial_update(self, request, pk=None):
        # PATCH METHOD
        pass

    @renderer_classes([JSONRenderer])
    def destroy(self, request, pk=None):
        # DELETE METHOD
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        url_count_changer(request, False)
        return MsgOk()

    def list(self, request):
        # GET ALL
        queryset = self.get_queryset().all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)
