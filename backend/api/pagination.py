from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "limit"


class EmptyResultsPagination(PageNumberPagination):
    page_size = 6  # или нужное вам значение
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": [{}],  # Всегда возвращаем пустой объект в results
            }
        )
