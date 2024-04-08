# 순서: 표준 라이브러리 모듈 -> 서드 파티 라이브러리 모듈 -> 로컬 프로젝트 모듈
import itertools
from typing import Dict, List

from django.contrib.gis.geoip2 import GeoIP2


def location_finder(request):
    return GeoIP2().country(request)


def dict_slice(d:Dict, n:int):
    return dict(itertools.islice(d.items(), n))


def dict_filter(d:Dict, filter_list:List):
    # 파라미터 값이 없을 경우
    if d is None:
        return {}

    filtered = {}
    for k, v in d.items():
        if k in filter_list:
            filtered[k] = v
    return filtered