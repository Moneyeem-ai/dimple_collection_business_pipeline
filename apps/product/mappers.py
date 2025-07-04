from apps.product.models import Product
from apps.department.models import Size, Color


def pt_entry_to_pt_entry_mapper(pt_entry, without_id=True, without_product_id=True, batch_id=None):
    mapped_data = {
        "id": pt_entry[0],
        "product_id": pt_entry[1],
        "size_id": pt_entry[7],
        "quantity": pt_entry[8],
        "color_id": pt_entry[9],
        "color_code": pt_entry[10],
        "mrp": pt_entry[11],
        "pur_price": None if batch_id is None else pt_entry[12],
        # "suffix": pt_entry[12],
        "invoice_number": pt_entry[13],
        "invoice_date": pt_entry[14],
    }
    if mapped_data["size_id"] == '':
        mapped_data["size_id"] = Size.objects.get_or_create(size_value="None")
    if mapped_data["color_id"] == '':
        mapped_data["color_id"] = Color.objects.get_or_create(color_name="None")
    if without_id:
        mapped_data.pop("id")
    if without_product_id:
        mapped_data.pop("product_id")
    return mapped_data


def pt_entry_to_product_mapper(pt_entry, without_id=True, without_images=True, without_metadata=True):
    if id:=pt_entry[1]:
        try:
            product = Product.objects.get(id=id)
            product_images = product.product_images
            metadata = product.metadata
        except:
            product_images = None
            metadata = {}
    else:
        product_images = None
        metadata = {}
    mapped_data = {
        "id": pt_entry[1],
        "article_number": pt_entry[2],
        "department_id": pt_entry[3],
        "category_id": pt_entry[4],
        "subcategory_id": pt_entry[5],
        "brand_id": pt_entry[6],
        "product_images": product_images,
        "metadata": metadata
    }
    if without_id:
        mapped_data.pop("id")
    if without_images:
        mapped_data.pop("product_images")
    if without_metadata:
        mapped_data.pop("metadata")
    return mapped_data


def z_order_upload_to_dict_mapper(row):
    return {
        "pt_entry_id": row[0],
        "department": row[1],
        "category": row[2],
        "subcategory": row[3],
        "article_number": row[4],
        "color_id": row[5],
        "size_id": row[6],
        "brand": row[7],
        "mrp": row[8],
        "pur_price": row[9],
        "barcode": row[10]
    }
