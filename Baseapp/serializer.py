from rest_framework import serializers
from .models import Product

class productserilzer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'sold_count', 'dicount_price']

    def validate(self, data):
        stock=data.get('stock', None)
        discount=data.get('dicount', None)
        price=data.get('price',None)
        image=data.get('image',None)
        if price is not None:
            if data['price'] < 0:
                raise serializers.ValidationError("Price cannot be negative.")
        if stock is not None:
            if data['stock'] and  data['stock'] < 0:
                raise serializers.ValidationError("Stock cannot be negative.")
        if discount is not None:
            if data['dicount'] and  data['dicount'] < 0 or data['dicount'] > 100:
                raise serializers.ValidationError("Discount must be between 0 and 100.")
        if image is not None:
            if data['image'].name.endswith(('.png', '.jpg', '.jpeg')) is not True:
                raise serializers.ValidationError("Image must be a PNG or JPG file.")
        return data
    
    def save(self, **kwargs):
        discount= kwargs.get('discount', None)
        if discount is not None:
            if kwargs['discount'] > 0:
                price = self.validated_data['price']
                discount = self.validated_data['discount']
                self.validated_data['discount_price']= price - (price * discount / 100)
        return super().save(**kwargs)