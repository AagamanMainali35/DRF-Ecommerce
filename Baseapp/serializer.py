from rest_framework import serializers
from .models import Product,Order,Order_item
from rest_framework.exceptions import ValidationError
import random
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
    
class Items_Serializer(serializers.ModelSerializer):
    prodcut_instance=productserilzer(read_only=True)
    product_id=serializers.CharField(write_only=True)
    class Meta:
        model=Order_item
        fields =['product_id','quantity','prodcut_instance']

class order_serilizer(serializers.ModelSerializer):
    order_items=Items_Serializer(many=True)
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_id=serializers.CharField(read_only=True)
    totalAmount=serializers.IntegerField(read_only=True)
    class Meta:
        model=Order
        fields=['order_id','customer','totalAmount','order_items']
        read_only_fields = ['order_date']	        
    def create(self, validated_data):
        order_items=validated_data.pop('order_items')
        validated_data['order_id']=f'ORD{random.randint(100000,999999)}'
        Total = 0
        for data in order_items:
            pr = Product.objects.get(id=data['product_id'])
            Total += pr.price * data['quantity']
        validated_data['totalAmount'] = Total
        order_ins=Order.objects.create(**validated_data)
        for data in order_items:
            pr=Product.objects.get(id=data['product_id'])
            Total+=pr.price*data['quantity']
            Order_item.objects.create(order_instance=order_ins,prodcut_instance=pr,quantity=data['quantity'])
        order_ins.save()
        return order_ins
    
    def update(self, instance, validated_data):
        order_items=validated_data.pop('order_items')
        total=0
        instance.order_items.all().delete()
        for data in order_items:
            pr=Product.objects.filter(id=data['product_id']).first()
            if pr is not None:
                pr_id=data['product_id']
                quantity=data['quantity']
                price=pr.price
                total+=price*data['quantity']
                Order_item.objects.create(order_instance=instance,prodcut_instance=pr,quantity=quantity)
            else:
                raise ValidationError(f"Product with id {data['product_id']} does not exist.")
        instance.totalAmount=total
        instance.save()   
        return instance
         
 