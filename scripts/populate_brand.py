import os

import pandas as pd

from config.settings.base import BASE_DIR
from apps.department.models import Brand

csv_file_path = os.path.join(BASE_DIR, 'data', 'brand_sheet.csv')
df = pd.read_csv(csv_file_path)

Brand.objects.all().delete()

for index, row in df.iterrows():
    brand, created = Brand.objects.get_or_create(brand_name=row['BRAND'], brand_code=row["CODE"])
