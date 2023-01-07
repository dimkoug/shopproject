import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


from shop.models import (
    Address,Category, Supplier, Brand, BrandSupplier, Feature,
    FeatureCategory, Attribute, Tag, Product, Shipment,
    ProductTag, ProductAttribute, ProductCategory,
    Media, Offer, OfferProduct, Order, OrderItem,
    ShoppingCart, Hero, HeroItem, Logo,Stock
)


from ..serializers import (
    AddressSerializer,CategorySerializer, TagSerializer, FeatureSerializer,
    AttributeSerializer, ProductSerializer, ShipmentSerializer,
    SupplierSerializer, BrandSerializer, MediaSerializer,
    LogoSerializer,StockSerializer, HeroSerializer,OfferSerializer,
    OrderSerializer
)

@api_view(['GET'])
def getStockList(request):
    query = request.query_params.get('keyword')
    object_list = Stock.objects.all()
    if query == None:
        query = ''
    print(query)
    if query and query != '':
        object_list = object_list.filter(name__icontains=query)
    
    page = request.query_params.get('page')
    print(page)
    paginator = Paginator(object_list,2)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    serializer = StockSerializer(object_list, many=True)
    return Response({'stock_list':serializer.data, 'page':page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getStock(request, pk):
    model = Stock
    obj = model.objects.get(id=pk)
    serializer = StockSerializer(obj)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createStock(request):
    model = Stock
    data = request.data
    obj = model.objects.create(**data)
    serializer = StockSerializer(obj, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateStock(request, pk):
    model = Stock
    try:
        obj = model.objects.get(id=pk)
        data = request.data
        obj.name = data['name']
        obj.save()
        serializer = StockSerializer(obj, many=False)
        return Response(serializer.data)
    except Stock.DoesNotExist:
        message = {'detail': f"{model.__name__} with id  {pk} not exists"}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteStock(request,pk):
    model = Stock
    try:
        forDeletetion = model.objects.get(id=pk)
        forDeletetion.delete()
        return Response(f'{model.__name__} was deleted')
    except Stock.DoesNotExist:
        message = {'detail': f"{model.__name__} with id {pk} not exists"}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)