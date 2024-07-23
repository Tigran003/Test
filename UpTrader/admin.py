from django.contrib import admin
from UpTrader.models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'menu_name', 'url')
    list_filter = ('menu_name', 'parent')
    search_fields = ('name',)
    ordering = ('parent', 'name')
