from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .permissions import IsAuthor

from .models import *
from .serializers import *


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'year', 'average_rating']

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("title", 
                          openapi.IN_QUERY, 
                          "search products by title", 
                          type=openapi.TYPE_STRING)])
    @action(methods=['GET'], detail=False)
    def search(self, request):
        title = request.query_params.get("title")
        queryset = self.get_queryset()
        if title:
            queryset = queryset.filter(title__icontains=title)

        serializer = MovieSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data, 200)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LikeViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['GET'])
    def toggle_like(self, request, pk):
        user = request.user
        movie = get_object_or_404(Movie, id=pk)

        if Like.objects.filter(user=user, movie=movie).exists():
            Like.objects.filter(user=user, movie=movie).delete()
        else:
            Like.objects.create(user=user, movie=movie)
        return Response("Like toggled", 200)

class FavoriteViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['GET'])
    def add_to_favorite(self, request, pk):
        user = request.user
        movie = get_object_or_404(Movie, id=pk)   
        favorited_obj = Favorite.objects.get(user=user, movie=movie)

        if favorited_obj.favorited == False:
            favorited_obj.favorited = not favorited_obj.favorited
            favorited_obj.save()
            return Response('Added to favorite')
        else:
            favorited_obj.favorited = not favorited_obj.favorited
            favorited_obj.save()
            return Response('Deleted from favorites')

class FavoriteView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(favorite__user=self.request.user, favorite__favorited=True)
        return queryset


@api_view(['POST'])
def add_rating(request, p_id):
    user = request.user
    movie = get_object_or_404(Movie, id=p_id)
    value = request.POST.get("value")

    if not user.is_authenticated:
        raise ValueError("authentication credentials are not provided")

    if not value:
        raise ValueError("value is required")
    
    if Rating.objects.filter(user=user, movie=movie).exists():
       rating = Rating.objects.get(user=user, movie=movie)
       rating.value = value
       rating.save()
    else:
        Rating.objects.create(user=user, movie=movie, value=value)

    return Response("rating created", 201)