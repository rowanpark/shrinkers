from datetime import timedelta

from django.db.models.aggregates import Count
from django.http import Http404  # 아래 표현 방식보다 더 일반적으로 흔하게 사용
# from django.http.response import Http404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from shortener.models import ShortenedUrls, Statistic
from shortener.urls.serializers import BrowserStatSerializer, UrlCreateSerializer, UrlListSerializer
from shortener.utils import MsgOk, get_kst, url_count_changer


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = ShortenedUrls.objects.all().order_by('-created_at')
#     serializer_class = UrlListSerializer
#     permission_classes = [permissions.IsAuthenticated]


class UrlListViewSet(viewsets.ModelViewSet):
    queryset = ShortenedUrls.objects.order_by('-created_at')
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        # POST METHOD
        serializer = UrlCreateSerializer(data=request.data)
        # print('serializer:', serializer)
        # print('serializer.is_valid():', serializer.is_valid())
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
        # print(pk, request.user.id)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        url_count_changer(request, False)
        return MsgOk()

    def list(self, request):
        # GET ALL
        queryset = self.get_queryset().filter(creator_id=request.user.id).all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def add_click(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        rtn = queryset.first().clicked()  # 메서드 체이닝
        serializer = UrlListSerializer(rtn)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reset_click(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        rtn = queryset.first().reseted_click()  # 메서드 체이닝
        serializer = UrlListSerializer(rtn)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def add_browser_today(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id).first()
        new_history = Statistic()
        new_history.record(request, queryset, {})
        return MsgOk()

    @action(detail=True, methods=['get'])
    def get_browser_stats(self, request, pk=None):
        queryset = Statistic.objects.filter(
            shortened_url_id=pk,
            shortened_url__creator_id=request.user.id,
            created_at__gte=get_kst() - timedelta(days=90),
        )
        if not queryset.exists():
            raise Http404
        # 1
        # browsers = (
        #     queryset.values('web_browser', 'created_at__date')
        #     .annotate(count=Count('id'))
        #     .values('count', 'web_browser', 'created_at__date')
        #     .order_by('-created_at__date')
        # )
        # 2
        browsers = (
            queryset.values('web_browser')
            .annotate(count=Count('id'))
            .values('count', 'web_browser')
            .order_by('-count')
        )
        # print('browsers:', browsers)
        serializer = BrowserStatSerializer(browsers, many=True)
        return Response(serializer.data)
