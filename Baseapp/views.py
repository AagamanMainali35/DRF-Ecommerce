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
from .serializer import productserailzer,Cart_serilizer
from rest_framework.pagination import PageNumberPagination
import requests
from django.shortcuts import redirect


@api_view(['POST'])
def login(requests):
    username=requests.data.get('username')
    password=requests.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        token=RefreshToken.for_user(user)
        return Response({
            "refresh_Token":str(token),
            "access_Token":str(token.access_token)
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

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
    Requested_data= productserailzer(data=request.data)
    if Requested_data.is_valid() is False:
        return Response({'error': Requested_data.errors, 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    else : 
        Requested_data.save() 
        return Response({'message':'Product Creation successful','status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    paginator_ins=PageNumberPagination()
    paginator_ins.page_size=10
    paginated_data=paginator_ins.paginate_queryset(products,request)
    serializer = productserailzer(paginated_data, many=True)
    return paginator_ins.get_paginated_response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_productById(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        serializer = productserailzer(product)
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
        validation=productserailzer(products,partial=True,data=request.data)
        if validation.is_valid():
            print(validation._validated_data)
            validation.save()
            return Response({'message':'update sucessfull','data':validation.data}, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({'message':'No product With fiven ID found', 'status':status.HTTP_404_NOT_FOUND})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    payload=Cart_serilizer(data=request.data,context={'request': request})
    if payload.is_valid():
        print(payload.validated_data)
        payload.save()
        return Response({'message':"Order has been placed sucessfully","status":status.HTTP_201_CREATED})
    else:
        errors = payload.errors
        first_key = next(iter(errors))
        message=payload.errors[first_key]    
        if isinstance(message, list):
            message=message[0]    
        return Response({'message': message, 'status': 400}, status=400)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getallOrders(request):
    User_Orders=Cart.objects.all()
    payload=Cart_serilizer(User_Orders,many=True)
    return Response(payload.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order(request,order_id):
    cart_data=Cart.objects.filter(order_id=order_id).first()
    if cart_data is None:
        return Response({'Message':f"No order assosiated with {order_id} was found","status":status.HTTP_404_NOT_FOUND})
    objects=Cart_serilizer(cart_data,partial=True,data=request.data)
    if objects.is_valid():
        objects.save()
        return Response({'Message':f"Order Updated Sucessfully","data":objects.data,"status":status.HTTP_200_OK})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteOrder(request,order_id):
    cart=Cart.objects.filter(order_id=order_id).first()
    if cart is not None:
        cart.delete()
        return Response({"message":f"Cart has been sucessfully deleted","status":status.HTTP_200_OK})
    else:
        return Response({"message":f"NO order  has been found","status":status.HTTP_404_NOT_FOUND})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chekout(request):
    url = "https://dev.khalti.com/api/v2/epayment/initiate/"
    headers = {
        "Authorization": "Key 2724d7c4030a42538ba3f91a68619b71",  
        "Content-Type": "application/json"
    }
    payload = {
        "return_url": f"http://127.0.0.1:8000/{reverse('verify')}",
        "website_url": "http://127.0.0.1:8000/",
        "amount": 1000, # Formula is alwys amount*100
        "purchase_order_id": "order123", #Genrate ID for each unique order
        "purchase_order_name": "Test Product", # alwaya Keep Your Order Name here
        "customer_info": { # put the user info over here no need foe all that hassle
            "name": "Test Bahadur",
            "email": "test@khalti.com",
            "phone": "9800000001"
        }
    }
    data=requests.post(url,headers=headers,json=payload)
    data=data.json()
    for key,value in data.items():
        print(f'{key}:{value}')
    if 'payment_url' in data:
        return Response({'payment_url':data['payment_url']})
    else: 
        return Response({'status':status.HTTP_408_REQUEST_TIMEOUT,'Messsage':'Please try again later......'})


@api_view(['GET'])
def verify(request):
    pidx=request.GET.get('pidx')
    if not pidx:
            return Response({'message':"Missing payment identifier please try again", 'status':status.HTTP_400_BAD_REQUEST})
    lookup_url = "https://dev.khalti.com/api/v2/epayment/lookup/"
    header={
        'Authorization':'key 2724d7c4030a42538ba3f91a68619b71',
        'Content-Type':'application/json'
    }
    payload={
        'pidx':pidx
    }
    data=requests.post(lookup_url,headers=header,json=payload)
    data=data.json()
    if data['status']=='Completed':
        # TODO: mark order as paid in your DB using purchase_order_id or pid
        return Response({'message':'Payment successful! Thank you.'})
    elif data['status'] == "Pending":
        return Response({'message':'Payment is pending. Please wait. Contact Khalti support for more details','status':status.HTTP_102_PROCESSING})
