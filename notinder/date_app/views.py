from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.db.models import Q
from .tasks import create_like, create_dislike


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class MostCompatibleUserAPIView(generics.RetrieveAPIView):
    serializer_class = MostCompatibleUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        gender_filter = 'female' if user.gender == 'male' else 'male'  # Определение фильтра по полу
        # Получение списка пользователей, которых пользователь уже лайкнул или дизлайкнул
        liked_and_disliked_users = Like.objects.filter(sender=user)
        # Выборка всех совместимостей, связанных с знаком пользователя
        compatibilities = Compatibility.objects.filter(
            Q(sign1=user.zodiac_sign) | Q(sign2=user.zodiac_sign)
        ).order_by('-weight')
        for compatibility in compatibilities:
            if compatibility.sign1 == user.zodiac_sign:
                compatible_sign = compatibility.sign2
            else:
                compatible_sign = compatibility.sign1
            # Выборка пользователей с приоритетным знаком
            compatible_users = CustomUser.objects.filter(
                zodiac_sign=compatible_sign, gender=gender_filter
            ).exclude(id__in=liked_and_disliked_users)
            # Если есть пользователь с приоритетным знаком, то возвращаем его, иначе переходим к след. знаку
            if compatible_users.exists():
                partner = compatible_users.first()
                return partner
        return None


class LikeUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user

        # Валидация данных из запроса
        serializer = LikeUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        liked_user_id = serializer.validated_data['user_id']

        try:
            liked_user = CustomUser.objects.get(id=liked_user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Отправить задачу на создание лайка в фоновом режиме
        create_like.delay(user.id, liked_user.id)

        return Response({"message": "Liked"}, status=status.HTTP_200_OK)


class DislikeUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        # Валидация данных из запроса
        serializer = DislikeUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        disliked_user_id = serializer.validated_data['user_id']
        try:
            disliked_user = CustomUser.objects.get(id=disliked_user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Отправить задачу на создание дизлайка в фоновом режиме
        create_dislike.delay(user.id, disliked_user.id)

        return Response({"message": "Disliked"}, status=status.HTTP_200_OK)
