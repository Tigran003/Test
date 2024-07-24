from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    url = models.CharField(max_length=200, blank=True, null=True)
    menu_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])

    def is_active(self, current_url):
        return self.get_absolute_url() == current_url

    def __str__(self):
        return self.name