from rest_framework import serializers
from .models import PTFileEntry, Product, ProductTagImage
from apps.department.models import Department


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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "department_name"]


class ProductTagImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTagImage
        fields = ["id", "product_image", "tag_image"]


class PTFileEntrySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
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
            "wsp",
            "status",
            "product_images",
        ]

    def get_product_images(self, obj):
        if obj.product and obj.product.product_images:
            # Assuming you have a serializer for ProductTagImage
            product_images_serializer = ProductTagImageSerializer(
                obj.product.product_images
            )
            print("this_product_images", product_images_serializer.data)
            return product_images_serializer.data
        return None


class PTFileEntryCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PTFileEntry
        fields = ["product_id", "size", "quantity", "color", "mrp", "wsp", "status"]

    def create(self, validated_data):
        product_id = validated_data.pop("product_id")
        product = Product.objects.get(id=product_id)
        pt_file_entry = PTFileEntry.objects.create(product=product, **validated_data)
        return pt_file_entry
