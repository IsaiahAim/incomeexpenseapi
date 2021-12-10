from rest_framework.pagination import PageNumberPagination


class ExpensePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    #max_page_size= 2
    #last_page_strings ="end"