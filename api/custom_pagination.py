from typing import Any

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data: Any) -> Response:
        return Response({
            'data': data,
            'links': {
                'current_page': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            }
        })
