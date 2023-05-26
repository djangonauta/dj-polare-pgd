import django_filters
from django import http


class QueryParamFilterSet(django_filters.FilterSet):

    @property
    def query_params(self):
        q = http.QueryDict(mutable=True)
        if self.form.is_valid():
            q.update({k: v for k, v in self.form.cleaned_data.items() if v})
            return q.urlencode()

        return ''
