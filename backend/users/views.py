from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.paginators import PageLimitPagination
from recipes.serializers import SubscriptionSerializer
from .models import CustomUser, Follow
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """
    Работа с пользователями.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageLimitPagination

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Такая подписка уже есть'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follow = Follow.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(
                follow,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if user == author:
            return Response(
                {'errors': 'Нельзя отписаться от себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Вы не подписаны на этого автора'},
            status=status.HTTP_400_BAD_REQUEST
        )
