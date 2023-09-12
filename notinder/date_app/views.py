from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.db.models import Q
from .tasks import create_like, create_dislike
from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'user': serializer.data,
            'access': access_token,
        }, status=status.HTTP_201_CREATED)

class MostCompatibleUserAPIView(generics.RetrieveAPIView):
    serializer_class = MostCompatibleUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        gender_filter = 'female' if user.gender == 'male' else 'male'  # Определение фильтра по полу
        # Получение списка пользователей, которых пользователь уже лайкнул или дизлайкнул
        liked_and_disliked_users = Like.objects.filter(sender=user).values_list('receiver', flat=True)
        # Выборка всех совместимостей, связанных с знаком пользователя
        compatibilities = Compatibility.objects.filter(
            Q(sign1=user.zodiac_sign) | Q(sign2=user.zodiac_sign)
        ).order_by('-weight')
        for compatibility in compatibilities:
            if compatibility.sign1 == user.zodiac_sign:
                compatible_sign = compatibility.sign2
            else:
                compatible_sign = compatibility.sign1
            # Выборка пользователей с приоритетным знаком, исключая лайкнутых и дизлайкнутых
            compatible_users = CustomUser.objects.filter(
                zodiac_sign=compatible_sign, gender=gender_filter
            ).exclude(id__in=liked_and_disliked_users)
            # Если есть пользователь с приоритетным знаком, то возвращаем его, иначе переходим к след. знаку
            if compatible_users.exists():
                partner = compatible_users.first()
                return partner
        return None


class LikeUserAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        liked_user = serializer.save()

        return Response({"message": "Liked"}, status=status.HTTP_200_OK)

class DislikeUserAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DislikeUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        disliked_user = serializer.save()

        return Response({"message": "Disliked"}, status=status.HTTP_200_OK)