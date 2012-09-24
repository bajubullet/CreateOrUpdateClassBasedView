class FeedDetailView(SupplierRequiredMixin, UpdateView):
    '''
    Detail(edit) view for feeds in front end.
    '''

    model = Feed
    form_class = FeedForm
    success_url = '/voedingsadvies/supplies/'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        else:
            return None
        try:
            obj = queryset.get()
            if obj.supplier.user != self.request.user:
                raise Http404
        except Feed.DoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def form_valid(self, form):
        feed = form.save(commit=False)
        supplier = Supplier.objects.get(user=self.request.user)
        feed.supplier = supplier
        feed.save()
        msg = _('Feed saved successfully.')
        messages.success(self.request, msg, fail_silently=True)
        return HttpResponseRedirect('/voedingsadvies/supplies/')

    def form_invalid(self, form):
        msg = _('Some error occurred while updating feed.')
        messages.error(self.request, msg, fail_silently=True)
        return super(FeedDetailView, self).form_invalid(form)