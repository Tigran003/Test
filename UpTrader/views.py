from django.views.generic import DetailView
from .models import Category


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'UpTrader/category_detail.html'
