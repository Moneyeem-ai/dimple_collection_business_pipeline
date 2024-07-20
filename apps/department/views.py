from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.list import ListView

from rest_framework import generics

from apps.department.models import Department, Category, SubCategory, Size, Brand
from apps.product.serializers import BrandSerializer, DepartmentSerializer


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


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class DepartmentListAPIView(generics.ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        queryset = Department.objects.all()
        department_names = self.request.query_params.get('department_names', None)
        exclude_names = self.request.query_params.get('exclude', None)
        
        if exclude_names:
            exclude_names_list = exclude_names.split(',')
            queryset = queryset.exclude(department_name__in=exclude_names_list)

        if department_names:
            department_names_list = department_names.split(',')
            queryset = queryset.filter(department_name__in=department_names_list)
            
        return queryset
