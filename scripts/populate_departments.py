import os

import pandas as pd

from config.settings.base import BASE_DIR
from apps.department.models import Department, Category, SubCategory

csv_file_path = os.path.join(BASE_DIR, 'data', 'departments_data.csv')
df = pd.read_csv(csv_file_path)

Department.objects.all().delete()

for index, row in df.iterrows():
    department, created = Department.objects.get_or_create(department_name=row['DEPARTMENT'])
    category, created = Category.objects.get_or_create(category_name=row['CATEGORY'], department=department, hsn_code=row['HSNCode'])
    sub_category, created = SubCategory.objects.get_or_create(subcategory_name=row['SUBCATEGORY'], category=category)
