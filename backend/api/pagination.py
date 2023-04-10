from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    # TODO: вынести в сеттингс хардкод
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 15
