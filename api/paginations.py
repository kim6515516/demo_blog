from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 7
    ordering = ('-id',)

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return '?page={}'.format(page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return '?page={}'.format(page_number)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total_pages': self.page.paginator.num_pages,
                'cur_page': self.page.number
            },
            'count': self.page.paginator.count,
            'results': data
        })


class StandardMinSizeResultsSetPagination(StandardResultsSetPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

