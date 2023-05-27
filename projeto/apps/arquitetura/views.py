from django.views import generic


class ElidedListView(generic.ListView):

    filter_class = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.request.GET.get(self.page_kwarg, 1)
        ctx['page_obj'].adjusted_elided_pages = ctx['paginator'].get_elided_page_range(page)
        if self.filter_class:
            ctx['filter'] = self.filter_class(self.request.GET)

        return ctx

    def get_queryset(self):
        if self.filter_class:
            return self.filter_class(self.request.GET, queryset=self.queryset).qs

        return super().get_queryset()
