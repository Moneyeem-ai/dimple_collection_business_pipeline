from django.urls import path

from apps.department.views import CategoriesByDepartmentView, SubCategoriesByCategoryView, SizesByDepartmentView

app_name = 'department'

urlpatterns = [
    path('api/categories/<int:department_id>/', CategoriesByDepartmentView.as_view(), name='categories_by_department'),
    path('api/subcategories/<int:category_id>/', SubCategoriesByCategoryView.as_view(), name='api_subcategories'),
    path('api/sizes/<int:department_id>/', SizesByDepartmentView.as_view(), name='api_sizes'),

]
