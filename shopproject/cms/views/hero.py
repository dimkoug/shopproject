from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.shortcuts import render
from django.apps import apps

from cms.cms_views import (
    BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)


from heroes.models import Hero


from heroes.forms import HeroForm, HeroItemForm


class HeroListView(BaseListView):
    model = Hero
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
    ]


class HeroDetailView(BaseDetailView):
    model = Hero
    queryset = Hero.objects.prefetch_related('heroitems')


class HeroCreateView(BaseCreateView):
    model = Hero
    form_class = HeroForm


class HeroUpdateView(BaseUpdateView):
    model = Hero
    form_class = HeroForm
    queryset = Hero.objects.prefetch_related('heroitems')



class HeroDeleteView(BaseDeleteView):
    model = Hero




def add_hero_item(request,hero_id):
    context = {}
    hero_item = Hero.objects.get(id=hero_id)
    form = HeroItemForm(request.POST or None,request=request,initial={'hero':hero_item})
    context['form'] = form
    template = 'cms/heroes/add_heroitem.html'
    if request.method == 'POST':
        form.save()
        return redirect(reverse_lazy('cms:hero-update',kwargs={"pk":hero_id}))


    return render(request,template,context) 
