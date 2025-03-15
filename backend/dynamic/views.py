from importlib import import_module
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.apps import apps
from django.db.models import Q, ForeignKey, ManyToManyField, ManyToOneRel, Prefetch

from dynamic.mixins import PaginationMixin, PassRequestToFormViewMixin
from dynamic.base_views import BaseListView, BaseDetailView,BaseCreateView,BaseUpdateView,BaseDeleteView

class DynamicListView(PaginationMixin, BaseListView):
    model = None
    paginate_by = settings.PAGINATED_ITEMS

    def get_queryset(self):
        queryset = None
        model_name = self.kwargs.get('model_name')
        if model_name:
            # Loop through all registered models to find the correct model
            for model in apps.get_models():
                if model.__name__.lower() == model_name.lower():
                    self.model = model
                    foreign_keys = [
                        field.name
                        for field in self.model._meta.get_fields()
                        if isinstance(field, ForeignKey)
                    ]

                    # Use select_related with all foreign keys
                    queryset = self.model.objects.all()
                    if foreign_keys:
                        queryset = queryset.select_related(*foreign_keys)
                    if hasattr(self.model, 'user'):
                        if not self.request.user.is_superuser:
                            queryset = queryset.filter(user_id=self.request.user.id)
        else:
            raise ValueError("Model name not provided or invalid")
        
        q = self.request.GET.get('search')
        q_objects = Q()
        if q and q != '':
            q = str(q.strip())
            for f in self.model._meta.get_fields():
                field_name = f.name
                field_class_name = f.__class__.__name__

                # Direct CharField or TextField search
                if field_class_name in ['CharField', 'TextField']:
                    q_obj = Q(**{f"{field_name}__contains": q})
                    q_objects |= q_obj
                
                # ForeignKey search on related model's CharField or TextField fields
                elif field_class_name == 'ForeignKey':
                    # Get the related model
                    related_model = f.related_model
                    for related_field in related_model._meta.get_fields():
                        if related_field.__class__.__name__ in ['CharField', 'TextField']:
                            q_obj = Q(**{f"{field_name}__{related_field.name}__contains": q})
                            q_objects |= q_obj

            queryset = queryset.filter(q_objects)

        return queryset



class DynamicDetailView(BaseDetailView):
    pass


class DynamicCreateView(PassRequestToFormViewMixin,BaseCreateView):

    def form_valid(self, form):
        # Attach the current user if the model has a `user` field
        if hasattr(self.model, 'user'):
            form.instance.user = self.request.user
        return super().form_valid(form)



class DynamicUpdateView(PassRequestToFormViewMixin,BaseUpdateView):
    pass


class DynamicDeleteView(BaseDeleteView):
    pass




