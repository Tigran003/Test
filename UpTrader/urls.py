# categories/urls.py

from django.urls import path
from .views import CategoryDetailView

urlpatterns = [
    path('<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
]
