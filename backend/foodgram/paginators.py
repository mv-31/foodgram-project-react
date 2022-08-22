from rest_framework.pagination import PageNumberPagination
from foodgram import settings


class PageLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = settings.PAGE_SIZE
