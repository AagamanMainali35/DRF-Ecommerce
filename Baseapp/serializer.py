from rest_framework import serializers
from .models import Product,Cart,Cart_item
from rest_framework.exceptions import ValidationError
from django.db import transaction
class productserailzer(serializers.ModelSerializer):
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
    prodcut_instance=productserailzer(read_only=True)
    product_id=serializers.CharField(write_only=True)
    class Meta:
        model=Cart_item
        fields =['product_id','quantity','prodcut_instance']

class Cart_serilizer(serializers.ModelSerializer):
    cart_items=Items_Serializer(many=True)
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    totalAmount=serializers.IntegerField(read_only=True)
    class Meta:
        model=Cart
        fields=['customer','totalAmount','cart_items']
        
    def validate(self, data):
        cart_items=data.get('cart_items')
        for items in cart_items:
            id=items.get('product_id')
            requested_quantity=items.get('quantity')
            product_instance=Product.objects.filter(id=id).first()
            if int(product_instance.stock)==0:
                raise serializers.ValidationError('Out of stock !')            
            if int(product_instance.stock) < int(requested_quantity):
                raise serializers.ValidationError(f' Only {product_instance.stock} avilable for this product')
        return data
        	            
    def create(self, validated_data):
        cartobj=Cart.objects.filter(customer=validated_data.get('customer')).first()
        user_items=Cart_item.objects.filter(cart_instance=cartobj)
        cart_items = validated_data.pop('cart_items', [])
        with transaction.atomic():
            if cartobj is None:
                cart_ins=Cart.objects.create(**validated_data,totalAmount=0)
                Total = 0
                for data in cart_items:
                    pr_id=data.get('product_id')
                    pr_ins=Product.objects.filter(id=pr_id).first()
                    if pr_ins is None:
                        raise serializers.ValidationError('Invalid Product ID')
                    else:
                        Cart_item.objects.create(prodcut_instance=pr_ins,cart_instance=cart_ins,quantity=data.get('quantity'))
                Total += pr_ins.price * data['quantity']
                print(f'the total is "{Total}"')
                cart_ins.totalAmount = Total
                cart_ins.save()
                return cart_ins
            else:
                for data in cart_items:
                    pr_id = data.get('product_id')
                    quantity = data.get('quantity')
                    exists = user_items.filter(prodcut_instance__id=pr_id).exists()
                    pr_ins = Product.objects.filter(id=pr_id).first()
                    newprice=0
                    if pr_ins is None:
                        raise serializers.ValidationError('Invalid Product ID')
                    if exists:
                        pr_detail=Product.objects.get(id=pr_id)
                        pr_obj=Cart_item.objects.get(cart_instance=cartobj,prodcut_instance=pr_detail)
                        new_quantity=quantity+pr_obj.quantity
                        newprice+=pr_detail.price*new_quantity
                        pr_obj.quantity=new_quantity
                        cartobj.totalAmount=newprice
                        cartobj.save()
                        pr_obj.save()
                    else:
                        cartobj.totalAmount += int(pr_ins.price) * int(quantity)
                        cartobj.save()
                        Cart_item.objects.create(prodcut_instance=pr_ins, cart_instance=cartobj, quantity=quantity)
        return cartobj

    def update(self, instance, validated_data):
        cart_items=validated_data.pop('cart_items')
        total=0
        instance.cart_items.all().delete()
        for data in cart_items:
            pr=Product.objects.filter(id=data['product_id']).first()
            if pr is not None:
                pr_id=data['product_id']
                quantity=data['quantity']
                price=pr.price
                total+=price*data['quantity']
                Cart_item.objects.create(cart_instance=instance,prodcut_instance=pr,quantity=quantity)
            else:
                raise ValidationError(f"Product with id {data['product_id']} does not exist.")
        instance.totalAmount=total
        instance.save()   
        return instance
         
 