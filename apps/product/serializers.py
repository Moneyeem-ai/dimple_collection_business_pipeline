from rest_framework import serializers
from .models import PTFileEntry, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','article_number','department', 'category', 'subcategory', 'brand']


class PTFileEntrySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = PTFileEntry
        fields = ['id', 'product', 'size', 'quantity', 'color', 'mrp', 'wsp', 'status']


class PTFileEntryCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PTFileEntry
        fields = ['product_id', 'size', 'quantity', 'color', 'mrp', 'wsp', 'status']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        pt_file_entry = PTFileEntry.objects.create(product=product, **validated_data)
        return pt_file_entry
