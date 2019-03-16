from django.db.models import Q

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


class FilterMixin(object):
    """Mixin that supports filtering based on specific fields."""

    def apply_filters(self, request, queryset):
        filter_fields = getattr(self, 'filter_fields', None)

        if not filter_fields:
            return queryset

        qset = Q()
        for key, value in request.query_params.items():
            if key in filter_fields:
                qset &= Q(**{key: value})

        return queryset.filter(qset).distinct()


class ReadOnlyModelListViewSet(ListModelMixin, GenericViewSet):
    """A viewset that provides default `list()` action."""
    pass
