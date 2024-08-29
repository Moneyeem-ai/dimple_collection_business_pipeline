import os
import json
from pathlib import Path

import google.generativeai as genai

from django.conf import settings

from apps.department.models import Department, Brand, Category, SubCategory, Size, Color
from apps.product.models import Product, ProductImage, PTFileEntry


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
        model_name="gemini-1.5-flash",
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
    colors = Color.objects.values("id", "color_name")

    prompt_parts = [
        image_parts[0],
        (
            "Extract the information from this cloth tag. "
            "Map the extracted data to our Product model field, those are - department, brand, color, article_number, size, mrp. "
            "The value of department can be any one out of these values - 2P SUIT, 5P SUIT, ANARKALI KURTA, BLAZER R NECK, BLAZER V NECK, BOTTOM, COTI, DARK INDO, FOOTWERE, INDO BOX, INDO WESTERN, JEANS, JODHPURI, KURTA COTI, KURTA PAJAMA, KURTA SHRUG H, ONLINE, PATHANI, SAFA STALL SET, SHERWANI, SHIRT, STALL, TIE, TROUSER, T-SHIRT, WAIST COAT SUIT or WOOLEN. "
            "The value of brand will be the manufacturer(MFG), Concept by, or the band name on the tag. "
            "The value of color will be the color of cloth mentioned on tag. "
            "The value of article_number will be the unqine code mentioned on tag. It's name can be mentioned as - sytle, d.no, or article. "
            "The value of mrp will be the price of product mentioned on tag. "
            "The value of size can be any one out of these 32, 34, 36, 38, 40, 42, 44"
            "Name of the fields will not be same exactly and you may not find all the fields but map the fields which you feel are best suited. "
            "The output you should give should only be the json, mapping the extracted data with the model Product fields. "
            "I am giving you the output format you need to follow that: "
            """{"department": "department_extracted_value", "brand": "brand_extracted_value", "color": "color_extracted_value", "article_number": "article_number_extracted_value", "size": "size_extracted_value", "mrp": "mrp_extracted_value"}"""
        ),
    ]
    response = model.generate_content(prompt_parts)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
    print(response.text)

    try:
        json_data = json.loads(response.text)
    except:
        log_string = response.text
        cleaned_string = log_string.replace('```json', '').replace('```', '')
        # json_content = json_content[8:]
        print(cleaned_string)
        json_data = json.loads(cleaned_string)

    if value := json_data.get("department", None):
        genai.configure(api_key="AIzaSyDTSQQxzIkyxVEDvuJ3AzO4RKQyE1MEC5g")
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
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
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
        genai.configure(api_key="AIzaSyDFybkT9jc_jzxUBqMSv728aaCtDeRpDGs")
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
        print("#######################################3")
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
        genai.configure(api_key="AIzaSyBzmKf-YPsnXfaKiZ6uA96Iv1GYNtO58Uo")
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
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
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

    if value := json_data.get("color", None):
        genai.configure(api_key="AIzaSyBwv2A_G2nPr2Uk-sFIut-jSm3LykY1Bgs")
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        try:
            colors_json = json.dumps(list(colors))
        except:
            colors_json = []
        print("!!!1234567!")
        print(value)
        prompt = f"Perform text matching. I am providing you a json of list of color_name and there id - {colors_json}. Match the provided list and check if '{value}' is present in color_name, it will not be same exactly, but its meaning should be similar. The output you should give should only be the matching json."
        prompt_parts = [prompt]
        response = model.generate_content(prompt_parts)
        print("!!!!")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5")
        print(response.text)
        try:
            colorjson_data = json.loads(response.text)
        except:
            none_color, _ = Color.objects.get_or_create(color_name="None")
            colorjson_data = {"id": none_color.id}

        try:
            json_data.pop("color")
            json_data["color_id"] = colorjson_data.get("id")
        except:
            none_color, _ = Color.objects.get_or_create(color_name="None")
            json_data["color_id"] = none_color.id
    else:
        none_color, _ = Color.objects.get_or_create(color_name="None")
        try:
            json_data.pop("color")
            json_data["color_id"] = none_color.id
        except:
            json_data["color_id"] = none_color.id
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
    print(json_data)
    return json_data


def clean_extracted_data(data, product_image_id):


    product_images = ProductImage.objects.get(id=product_image_id)
    valid_keys = [
        field.name.replace("department", "department_id").replace("brand", "brand_id").replace("size", "size_id")
        for field in Product._meta.get_fields()
    ]
    valid_data = {key: data[key] for key in valid_keys if key in data}
    if product_images.metadata:
        if color:=product_images.metadata.get("color"):
            data["color_id"] = Color.objects.filter(color_name__icontains=color).first().id
    valid_data.update(
        {
            "metadata": data,
            "product_images": product_images,
        }
    )
    department = Department.objects.get_or_create(department_name="None")[0]
    valid_data["article_number"] = (
        valid_data["article_number"].upper()
        if valid_data["article_number"]
        else valid_data["article_number"]
    )
    valid_data["category"] = Category.objects.get_or_create(
        category_name="None", department=department
    )[0]
    valid_data["subcategory"] = SubCategory.objects.get_or_create(
        subcategory_name="None", category=valid_data["category"]
    )[0]
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7")
    print(valid_data)
    if product_images.metadata:
        if artcile_number:=product_images.metadata.get("article_number"):
            valid_data["article_number"] = artcile_number.upper()
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
            article_number = article_number.replace(" ", "").upper()
            product, _ = Product.objects.get_or_create(
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


def check_product_is_unique_or_merge(pt_entry_ids):


    processed_pt_entry = []
    for pt_entry_id in pt_entry_ids:
        if pt_entry_id not in processed_pt_entry:
            product = PTFileEntry.objects.get(id=pt_entry_id).product
            if product.id:
                similar_products = (
                    Product.objects.filter(
                        department=product.department,
                        category=product.category,
                        subcategory=product.subcategory,
                        article_number=product.article_number,
                        brand=product.brand,
                    )
                    .exclude(id=product.id)
                    .values_list("id", flat=True)
                )
                if len(similar_products) > 0:
                    associated_pt_entries = PTFileEntry.objects.filter(
                        product_id__in=similar_products
                    )
                    associated_pt_entries.update(product=product)
                    associated_pt_entry_ids = associated_pt_entries.values_list(
                        "id", flat=True
                    )
                    processed_pt_entry = list(processed_pt_entry) + list(associated_pt_entry_ids)
                    processed_pt_entry.append(pt_entry_id)
                    Product.objects.filter(id__in=similar_products).delete()
