from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .utility import generate_profile_id, checkpass , check_field
from django.urls import reverse
from django.db.models import Q
from .serializer import productserilzer,order_serilizer


@api_view(['POST'])
def signup(requests):
    email = requests.data.get('email')
    password = requests.data.get('password')
    first_name = requests.data.get('first_name')
    last_name = requests.data.get('last_name')
    gender = requests.data.get('gender')
    missing_fields = ['email', 'password', 'first_name', 'last_name']
    result=check_field(requests, *missing_fields)
    if result is not None:
        return result
    if checkpass(password) is not None:
        return Response({"error": checkpass(password),"status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(Q(email=email) | Q(username=email)).exists():
        return Response({"error": "Email or Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        profile_id=generate_profile_id()
        user_model=User.objects.create(email=email, username=email, first_name=first_name, last_name=last_name)
        user_model.set_password(password)
        user_model.save()
        Profile.objects.create(user=user_model,profile_id=profile_id,gender=gender)
        login_url= f'http://127.0.0.1:8000{reverse("token_obtain_pair")}'
        return Response({"message": f"Signup completed for {email}","login_url": login_url})

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_product(request):
    Requested_data= productserilzer(data=request.data)
    if Requested_data.is_valid() is False:
        return Response({'error': Requested_data.errors, 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    else : 
        Requested_data.save() 
        return Response({'message':'Product Creation successful','status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = productserilzer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_productById(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        serializer = productserilzer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND    )

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_Product(request,id):
    try:
        product=Product.objects.get(id=id)
        product.delete()
        return Response({'message': 'Product deleted successfully','status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
permission_classes([IsAuthenticated])
@api_view(['PATCH'])
def update_product(request, id):
    try:
        products=Product.objects.get(id=id)
        validation=productserilzer(products,partial=True,data=request.data)
        if validation.is_valid():
            print(validation._validated_data)
            validation.save()
            return Response({'message':'update sucessfull','data':validation.data}, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({'message':'No product With fiven ID found', 'status':status.HTTP_404_NOT_FOUND})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    payload=order_serilizer(data=request.data,context={'request': request})
    if payload.is_valid():
        print(payload.validated_data)
        payload.save()
        return Response({'message':"Order has been placed sucessfully","status":status.HTTP_201_CREATED})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getallOrders(request):
    User_Orders=Order.objects.all()
    payload=order_serilizer(User_Orders,many=True)
    return Response(payload.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order(request,order_id):
    Order_data=Order.objects.filter(order_id=order_id).first()
    if Order_data is None:
        return Response({'Message':f"No order assosiated with {order_id} was found","status":status.HTTP_404_NOT_FOUND})
    objects=order_serilizer(Order_data,partial=True,data=request.data)
    if objects.is_valid():
        objects.save()
        return Response({'Message':f"Order Updated Sucessfully","data":objects.data,"status":status.HTTP_200_OK})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteOrder(request,order_id):
    orders=Order.objects.filter(order_id=order_id).first()
    if orders is not None:
        orders.delete()
        return Response({"message":f"Order no - {order_id} has been sucessfully deleted","status":status.HTTP_200_OK})

    else:
        return Response({"message":f"NO order with id {order_id} has been found","status":status.HTTP_404_NOT_FOUND})
    
    
