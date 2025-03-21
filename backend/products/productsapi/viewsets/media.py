import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


from media.models import Media


from ..serializers import MediaSerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# @api_view(['GET'])
# def getMediaList(request):
#     query = request.query_params.get('keyword')
#     object_list = Media.objects.all()
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
#     serializer = MediaSerializer(object_list, many=True)
#     return Response({'media_list':serializer.data, 'page':page, 'pages': paginator.num_pages})


# @api_view(['GET'])
# def getMedia(request, pk):
#     model = Media
#     obj = model.objects.get(id=pk)
#     serializer = MediaSerializer(obj)
#     return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def createMedia(request):
#     model = Media
#     data = request.data
#     obj = model.objects.create(**data)
#     serializer = MediaSerializer(obj, many=False)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['PUT'])
# @permission_classes([IsAdminUser])
# def updateMedia(request, pk):
#     model = Media
#     try:
#         obj = model.objects.get(id=pk)
#         data = request.data
#         obj.name = data['name']
#         obj.save()
#         serializer = MediaSerializer(obj, many=False)
#         return Response(serializer.data)
#     except Media.DoesNotExist:
#         message = {'detail': f"{model.__name__} with id  {pk} not exists"}
#         return Response(message,status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def deleteMedia(request,pk):
#     model = Media
#     try:
#         forDeletetion = model.objects.get(id=pk)
#         forDeletetion.delete()
#         return Response(f'{model.__name__} was deleted')
#     except Media.DoesNotExist:
#         message = {'detail': f"{model.__name__} with id {pk} not exists"}
#         return Response(message,status=status.HTTP_400_BAD_REQUEST)