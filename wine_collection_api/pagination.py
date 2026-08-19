from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """Standard pagination for most endpoints."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200


class CollectionPagination(PageNumberPagination):
    """Pagination for collections."""
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentPagination(PageNumberPagination):
    """Pagination for comments."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProviderPagination(PageNumberPagination):
    """Pagination for providers."""
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
