from django.contrib.staticfiles.storage import StaticFilesStorage
from django_weasyprint import WeasyTemplateResponseMixin
from rest_framework import response, status


class SelectSerializerFieldsMixin:

    param_field_names = 'field_names'

    def to_representation(self, data):
        data = super(SelectSerializerFieldsMixin, self).to_representation(data)
        fields = self.context['request'].query_params.get(self.param_field_names, None)
        if fields:
            fields = set(fields.split(','))
            data = {k: v for k, v in data.items() if k in fields}

        return data


class PaginatedResponseMixin:

    def build_paginated_response(self, objects):
        page = self.paginate_queryset(objects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(objects, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class BaseReportResponseMixin(WeasyTemplateResponseMixin):

    static_files_storage = StaticFilesStorage()

    pdf_stylesheets = [
        static_files_storage.path('css/normalize.min.css'),
        static_files_storage.path('css/paper.min.css'),
    ]
