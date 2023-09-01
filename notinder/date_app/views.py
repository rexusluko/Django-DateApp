from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.db.models import Q
from .photo import save_photo_to_minio

class CreateUserAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        if data['photo']:
            print("AAA")
            photo_path = save_photo_to_minio(data.pop('photo').pop())
        else:
            photo_path = 'no photo'
        data['photo_path'] = photo_path
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class MostCompatibleUserAPIView(generics.RetrieveAPIView):
    serializer_class = MostCompatibleUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        gender_filter = 'female' if user.gender == 'male' else 'male'  # Определение фильтра по полу
        # Получение списка пользователей, которых пользователь уже лайкнул или дизлайкнул
        liked_users = Like.objects.filter(sender=user).values_list('receiver', flat=True)
        disliked_users = Like.objects.filter(sender=user, is_liked=False).values_list('receiver', flat=True)
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
            ).exclude(id__in=liked_users).exclude(id__in=disliked_users)
            # Если есть пользователь с приоритетным знаком, то возвращаем его, иначе переходим к след. знаку
            if compatible_users.exists():
                partner = compatible_users.first()
                return partner
        return None


class LikeUserAPIView(APIView):
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

        like = Like.objects.create(sender=user, receiver=liked_user, is_liked=True)
        if Like.objects.filter(sender=liked_user, receiver=user, is_liked=True).exists():
            Match.objects.create(friend1=user, friend2=liked_user)
            return Response({"message": "Liked and matched"}, status=status.HTTP_200_OK)

        return Response({"message": "Liked"}, status=status.HTTP_200_OK)

class DislikeUserAPIView(APIView):
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

        dislike = Like.objects.create(sender=user, receiver=disliked_user, is_liked=False)

        return Response({"message": "Disliked"}, status=status.HTTP_200_OK)
