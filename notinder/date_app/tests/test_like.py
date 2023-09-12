import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from date_app.models import ZodiacSign, Compatibility


@pytest.mark.django_db
def test_like(api_client):
    zodiac_cancer = ZodiacSign.objects.create(name="Cancer")
    zodiac_leo = ZodiacSign.objects.create(name="Leo")
    zodiac_virgo = ZodiacSign.objects.create(name="Virgo")

    Compatibility.objects.create(sign1=zodiac_cancer, sign2=zodiac_leo, weight=8)
    Compatibility.objects.create(sign1=zodiac_cancer, sign2=zodiac_virgo, weight=6)

    main_user = {
        "username": "new_boy5",
        "password": "1234",
        "gender": "male",
        "email": "new_boy5@example.com",
        "zodiac_sign": "Cancer",
        "description": "I'm a user",
    }
    api_client.post(reverse('register'), main_user)
    most_compatible_user = {
        "username": "new_girl3",
        "password": "1234",
        "gender": "female",
        "email": "new_girl3@example.com",
        "zodiac_sign": "Leo",
        "description": "I'm a user",
    }
    api_client.post(reverse('register'), most_compatible_user)
    less_compatible_user = {
        "username": "bad_girl6",
        "password": "1234",
        "gender": "female",
        "email": "bad_girl6@example.com",
        "zodiac_sign": "Virgo",
        "description": "I'm a user",
    }
    api_client.post(reverse('register'), less_compatible_user)

    token1_data = {
        "username": main_user["username"],
        "password": main_user["password"]
    }
    headers1 = {"Authorization": f"Bearer {api_client.post(reverse('token'), token1_data).data['access']}"}

    find1_response = api_client.get(reverse('find-partner'), headers=headers1)

    like1_response = api_client.post(reverse('like'), {"user_id": find1_response.data["id"]}, headers=headers1)
    print(like1_response.data)
    assert like1_response.data["message"] == "Liked"

    token2_data = {
        "username": most_compatible_user["username"],
        "password": most_compatible_user["password"]
    }
    headers2 = {"Authorization": f"Bearer {api_client.post(reverse('token'), token2_data).data['access']}"}

    find2_response = api_client.get(reverse('find-partner'), headers=headers2)

    like2_response = api_client.post(reverse('like'), {"user_id": find2_response.data["id"]}, headers=headers2)
    assert like2_response.data["message"] == "Liked"

    find3_response = api_client.get(reverse('find-partner'), headers=headers1)
    dislike_response = api_client.post(reverse('dislike'), {"user_id": find3_response.data["id"]}, headers=headers1)
    assert dislike_response.data["message"] == "Disliked"

