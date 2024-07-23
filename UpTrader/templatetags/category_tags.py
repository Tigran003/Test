# templatetags/category_tags.py
from django import template
from django.template.loader import render_to_string
from UpTrader.models import Category

register = template.Library()

@register.simple_tag
def get_categories_for_menu(menu_name):
    """
    Fetch categories for a specific menu by name.
    """
    return Category.objects.filter(menu_name=menu_name).select_related('parent').prefetch_related('children')

def build_category_tree(categories, current_url):
    """
    Build the category tree structure.
    """
    category_dict = {cat.id: cat for cat in categories}
    top_level_categories = [cat for cat in categories if cat.parent_id is None]
    children_dict = {cat.id: [] for cat in categories}

    for category in categories:
        if category.parent_id is not None:
            children_dict[category.parent_id].append(category)

    def add_children(category):
        category.children = children_dict.get(category.id, [])
        for child in category.children:
            add_children(child)

    for category in top_level_categories:
        add_children(category)

    def mark_active(category, current_url):
        category.is_active = category.get_absolute_url() == current_url
        category.is_expanded = category.is_active
        for child in category.children:
            mark_active(child, current_url)
            if child.is_expanded:
                category.is_expanded = True

    def expand_all_above(category):
        if category.parent:
            category.parent.is_expanded = True
            expand_all_above(category.parent)

    for category in top_level_categories:
        mark_active(category, current_url)

    for category in top_level_categories:
        expand_all_above(category)

    def expand_first_level_children(category):
        if category.is_active or any(child.is_expanded for child in category.children):
            for child in category.children:
                child.is_expanded = True
                expand_first_level_children(child)

    for category in top_level_categories:
        expand_first_level_children(category)

    return top_level_categories

@register.simple_tag(takes_context=True)
def draw_category_tree_html(context, menu_name):
    categories = get_categories_for_menu(menu_name)
    current_url = context['request'].path
    category_tree = build_category_tree(categories, current_url)
    return render_to_string('UpTrader/category_tree.html', {'categories': category_tree, 'current_url': current_url})
