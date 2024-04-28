from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.list import ListView

from apps.department.models import Category, SubCategory, Size

# Create your views here.

class CategoriesByDepartmentView(ListView):
    model = Category

    def get_queryset(self):
        department_id = self.kwargs['department_id']
        return Category.objects.filter(department_id=department_id)

    def render_to_response(self, context, **response_kwargs):
        category_list = context['object_list']
        data = [{'id': category.id, 'name': category.category_name} for category in category_list]
        return JsonResponse(data, safe=False)
    

class SubCategoriesByCategoryView(ListView):
    model = SubCategory

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return SubCategory.objects.filter(category_id=category_id)

    def render_to_response(self, context, **response_kwargs):
        subcategory_list = context['object_list']
        data = [{'id': sub.id, 'name': sub.subcategory_name} for sub in subcategory_list]
        return JsonResponse(data, safe=False)

class SizesByDepartmentView(ListView):
    model = Size

    def get_queryset(self):
        department_id = self.kwargs['department_id']
        return Size.objects.filter(department_id=department_id)

    def render_to_response(self, context, **response_kwargs):
        size_list = context['object_list']
        data = [{'id': size.id, 'value': size.size_value} for size in size_list]
        return JsonResponse(data, safe=False)