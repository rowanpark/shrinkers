# import datetime
from datetime import datetime, timedelta, timezone
from django.db.models import F
# from django.http import JsonResponse  # 아래 표현 방식보다 더 일반적으로 흔하게 사용
# from django.http.response import JsonResponse

from rest_framework.response import Response

from shortener.models import Users


def url_count_changer(request, is_increase: bool):
    count_number = 1 if is_increase else -1
    ### 1
    Users.objects.filter(user_id=request.user.id).update(url_count=F('url_count') + count_number)
    ### 2
    # user = Users.objects.get(id=request.user.id)
    # Users.objects.filter(user=user).update(url_count=F('url_count') + count_number)


def MsgOk(status: int = 200):
    # return JsonResponse(status=status, data=dict(msg='ok'))
    return Response({'msg': 'ok'}, status=status)


def get_kst():
    # return datetime.utcnow() + timedelta(hours=9)
    return datetime.now(timezone.utc) + timedelta(hours=9)
