import datetime
from django.shortcuts import render
import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


from shop.models import Product


from ..serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# @api_view(['GET'])
# def getProductList(request):
#     query = request.query_params.get('keyword')
#     serializer_context = {
#             'request': request,
#     }
#     object_list = Product.objects.all()
#     if query == None:
#         query = ''
#     print(query)
#     if query and query != '':
#         object_list = object_list.filter(name__icontains=query)
    
#     page = request.query_params.get('page')
#     print(page)
#     paginator = Paginator(object_list,2)
#     try:
#         object_list = paginator.page(page)
#     except PageNotAnInteger:
#         object_list = paginator.page(1)
#     except EmptyPage:
#         object_list = paginator.page(paginator.num_pages)
#     if page == None:
#         page = 1
#     page = int(page)
#     serializer = ProductSerializer(object_list, many=True,context=serializer_context)
#     return Response({'product_list':serializer.data, 'page':page, 'pages': paginator.num_pages})


# @api_view(['GET'])
# def getProduct(request, pk):
#     model = Product
#     obj = model.objects.get(id=pk)
#     serializer = ProductSerializer(obj)
#     return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def createProduct(request):
#     model = Product
#     data = request.data
#     obj = model.objects.create(**data)
#     serializer = ProductSerializer(obj, many=False)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['PUT'])
# @permission_classes([IsAdminUser])
# def updateProduct(request, pk):
#     model = Product
#     try:
#         obj = model.objects.get(id=pk)
#         data = request.data
#         obj.name = data['name']
#         obj.save()
#         serializer = ProductSerializer(obj, many=False)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         message = {'detail': f"{model.__name__} with id  {pk} not exists"}
#         return Response(message,status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def deleteProduct(request,pk):
#     model = Product
#     try:
#         forDeletetion = model.objects.get(id=pk)
#         forDeletetion.delete()
#         return Response(f'{model.__name__} was deleted')
#     except Product.DoesNotExist:
#         message = {'detail': f"{model.__name__} with id {pk} not exists"}
#         return Response(message,status=status.HTTP_400_BAD_REQUEST)