from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500


class LargePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500


class UnlimitedPagination(PageNumberPagination):
    """
    Admin panel uchun — barcha ma'lumotni bir sahifada qaytaradi.
    Response strukturasi saqlanadi: { count, next, previous, results: [...] }
    """
    page_size = 10_000
    page_size_query_param = 'page_size'
    max_page_size = 10_000
