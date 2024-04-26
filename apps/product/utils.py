import os
import json
from pathlib import Path

import google.generativeai as genai

from django.conf import settings

from apps.department.models import Department, Brand, Category, SubCategory, Size
from apps.product.models import Product, ProductImage


def extract_data_from_tag(image_path):
    print("debug_is_on")
    genai.configure(api_key="AIzaSyAHs5fgDlrSyGLyw1eUPvXSrEWacqnR94s")

    # Set up the model
    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro-vision-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    # Validate that an image is present
    PATH = os.path.join(settings.MEDIA_ROOT, "tag_images", image_path)

    if not (img := Path(PATH)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {"mime_type": "image/png", "data": Path(PATH).read_bytes()},
    ]

    departments = Department.objects.values("id", "department_name")
    brands = Brand.objects.values("id", "brand_name")
    sizes = Size.objects.values("id", "size_value")

    prompt_parts = [
        image_parts[0],
        (
            "Extract the information from this cloth tag. "
            "Map the extracted data to our Product model field, those are - department, brand, color, article_number, size, mrp. "
            "The value of department can be - 2P SUIT, 5P SUIT, ANARKALI KURTA, BLAZER R NECK, BLAZER V NECK, BOTTOM, COTI, DARK INDO, FOOTWERE, INDO BOX, INDO WESTERN, JEANS, JODHPURI, KURTA COTI, KURTA PAJAMA, KURTA SHRUG H, ONLINE, PATHANI, SAFA STALL SET, SHERWANI, SHIRT, STALL, TIE, TROUSER, T-SHIRT, WAIST COAT SUIT or WOOLEN. "
            "The value of brand will be the manufacturer(MFG), Concept by, or the band name on the tag. "
            "The value of color will be the color of cloth mentioned on tag. "
            "The value of article_number will be the unqine code mentioned on tag. It's name can be mentioned as - sytle, d.no, or article. "
            "The value of mrp will be the price of product mentioned on tag. "
            "The value of size can be 32, 34, 36, 38, 40, 42, 44"
            "Name of the fields will not be same exactly and you may not find all the fields but map the fields which you feel are best suited. "
            "The output you should give should only be the json, mapping the extracted data with the model Product fields. "
        ),
    ]
    response = model.generate_content(prompt_parts)
    print(response.text)

    try:
        json_data = json.loads(response.text)
    except:
        json_content = response.text.strip("`\n")
        json_content = json_content[8:]
        json_data = json.loads(json_content)

    if value := json_data.get("department", None):
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        try:
            departments_json = json.dumps(list(departments))
        except:
            departments_json = []
        value = value.lower()
        prompt = f"Perform text matching. I am providing you a json of list of department_name and there id - {departments_json}. Match the provided list and check if '{value}' is present in department_name, it will not be same exactly, but its meaning should be similar. The output you should give should only be the matching json."
        prompt_parts = [prompt]
        response = model.generate_content(prompt_parts)
        print(response.text)
        try:
            djson_data = json.loads(response.text)
        except:
            none_department, _ = Department.objects.get_or_create(
                department_name="None"
            )
            djson_data = {"id": none_department.id}

        try:
            json_data.pop("department")
            json_data["department_id"] = djson_data.get("id")
        except:
            none_department, _ = Department.objects.get_or_create(
                department_name="None"
            )
            json_data["department_id"] = none_department.id
    else:
        none_department, _ = Department.objects.get_or_create(department_name="None")
        try:
            json_data.pop("department")
            json_data["department_id"] = none_department.id
        except:
            json_data["department_id"] = none_department.id

    print("****")

    if value := json_data.get("brand", None):
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        try:
            brands_json = json.dumps(list(brands))
        except:
            brands_json = []
        value = value.lower()
        prompt = f"Perform text matching. I am providing you a json of list of brand_name and there id - {brands_json}. Match the provided list and check if '{value}' is present in brand_name, it will not be same exactly, but its meaning should be similar. The output you should give should only be the matching json."
        prompt_parts = [prompt]
        response = model.generate_content(prompt_parts)
        print("!!!!")
        print(response.text)
        try:
            bjson_data = json.loads(response.text)
        except:
            none_brand, _ = Brand.objects.get_or_create(brand_name="None")
            bjson_data = {"id": none_brand.id}

        try:
            json_data.pop("brand")
            json_data["brand_id"] = bjson_data.get("id")
        except:
            none_brand, _ = Brand.objects.get_or_create(brand_name="None")
            json_data["brand_id"] = none_brand.id
    else:
        none_brand, _ = Brand.objects.get_or_create(brand_name="None")
        try:
            json_data.pop("brand")
            json_data["brand_id"] = none_brand.id
        except:
            json_data["brand_id"] = none_brand.id

    if value := json_data.get("size", None):
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        try:
            sizes_json = json.dumps(list(sizes))
        except:
            sizes_json = []
        print("!!!1234567!")
        print(value)
        prompt = f"Perform text matching. I am providing you a json of list of size_value and there id - {sizes_json}. Match the provided list and check if '{value}' is present in size_value, it will not be same exactly, but its meaning should be similar. The output you should give should only be the matching json."
        prompt_parts = [prompt]
        response = model.generate_content(prompt_parts)
        print("!!!!")
        print(response.text)
        try:
            sjson_data = json.loads(response.text)
        except:
            none_size, _ = Size.objects.get_or_create(size_value="None")
            sjson_data = {"id": none_size.id}

        try:
            json_data.pop("size")
            json_data["size_id"] = sjson_data.get("id")
        except:
            none_size, _ = Size.objects.get_or_create(size_value="None")
            json_data["size_id"] = none_size.id
    else:
        none_size, _ = Size.objects.get_or_create(size_value="None")
        try:
            json_data.pop("size")
            json_data["size_id"] = none_size.id
        except:
            json_data["size_id"] = none_size.id
    print(json_data)
    return json_data


def clean_extracted_data(data, product_image_id):
    valid_keys = [
        field.name.replace("department", "department_id").replace("brand", "brand_id")
        for field in Product._meta.get_fields()
    ]
    valid_data = {key: data[key] for key in valid_keys if key in data}
    valid_data.update(
        {
            "metadata": data,
            "product_images": ProductImage.objects.get(id=product_image_id), 
        }
    )
    department = Department.objects.get_or_create(department_name="None")[0]
    valid_data["category"] = Category.objects.get_or_create(
        category_name="None", department=department
    )[0]
    valid_data["subcategory"] = SubCategory.objects.get_or_create(
        subcategory_name="None", category=valid_data["category"]
    )[0]
    return valid_data


def get_or_create_product(valid_data):
    department = Department.objects.get(id=valid_data.get("department_id"))
    brand = Brand.objects.get(id=valid_data.get("brand_id"))
    article_number = valid_data.get("article_number")
    if (
        department.department_name != "None"
        and brand.brand_name != "None"
        and article_number != None
    ):
        try:
            product, created = Product.objects.get_or_create(
                department=department,
                article_number=article_number,
                brand=brand,
            )
            for key, value in valid_data.items():
                setattr(product, key, value)
            product.save()
            return product
        except Exception as e:
            raise e
    try:
        product = Product.objects.create(**valid_data)
        return product
    except Exception as e:
        raise e
