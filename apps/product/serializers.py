from rest_framework import serializers

from .models import PTFileEntry, Product, ProductImage
from apps.department.models import Department, Category, SubCategory, Brand, Size, Color


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "article_number",
            "department",
            "category",
            "subcategory",
            "brand",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product_image", "tag_image"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "prefix", "department_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "department", "prefix", "category_name", "hsn_code"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "category", "prefix", "subcategory_name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "brand_name", "brand_code", "supplier_name"]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id", "department", "size_value"]

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["id", "color_name"]


class ProductReadSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "article_number",
            "department",
            "category",
            "subcategory",
            "brand",
        ]


class PTFileEntrySerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    product_images = serializers.SerializerMethodField()

    class Meta:
        model = PTFileEntry
        fields = [
            "id",
            "product",
            "size",
            "quantity",
            "color",
            "mrp",
            "pur_price",
            "invoice_number",
            "invoice_date",
            "status",
            "product_images",
        ]

    def get_product_images(self, obj):
        if obj.product and obj.product.product_images:
            product_images_serializer = ProductImageSerializer(
                obj.product.product_images
            )
            return product_images_serializer.data
        return None


class PTFileEntryCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    size_id = serializers.IntegerField(write_only=True)
    color_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PTFileEntry
        fields = [
            "id",
            "product_id",
            "size_id",
            "quantity",
            "color_id",
            "mrp",
            "pur_price",
            "invoice_number",
            "invoice_date",
            "status",
        ]

    def create(self, validated_data):
        product_id = validated_data.pop("product_id")
        product = Product.objects.get(id=product_id)
        print("creating product")
        pt_file_entry = PTFileEntry.objects.create(product=product, **validated_data)
        return pt_file_entry


class SubCategoryNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "subcategory_name"]


class CategoryNestedSerializer(serializers.ModelSerializer):
    subcategories = SubCategoryNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "category_name", "subcategories"]


class SizeNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id", "size_value"]


class DepartmentNestedSerializer(serializers.ModelSerializer):
    categories = CategoryNestedSerializer(many=True, read_only=True)
    sizes = SizeNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ["id", "department_name", "categories", "sizes"]
