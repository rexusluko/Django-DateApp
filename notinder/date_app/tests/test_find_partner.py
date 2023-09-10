import pytest
from django.urls import reverse
from date_app.models import ZodiacSign, Compatibility


@pytest.mark.django_db
def test_find_partner(api_client):
    zodiac_cancer = ZodiacSign.objects.create(name="Cancer")
    zodiac_leo = ZodiacSign.objects.create(name="Leo")
    zodiac_virgo = ZodiacSign.objects.create(name="Virgo")
    zodiac_aries = ZodiacSign.objects.create(name="Aries")

    Compatibility.objects.create(sign1=zodiac_cancer, sign2=zodiac_leo, weight=8)
    Compatibility.objects.create(sign1=zodiac_cancer, sign2=zodiac_virgo, weight=6)
    Compatibility.objects.create(sign1=zodiac_cancer, sign2=zodiac_aries, weight=10)

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
    same_gender_user = {
        "username": "bad_boy2",
        "password": "1234",
        "gender": "male",
        "email": "bad_boy2@example.com",
        "zodiac_sign": "Aries",
        "description": "I'm a user",
    }
    api_client.post(reverse('register'), same_gender_user)
    token_data = {
        "username": main_user["username"],
        "password": main_user["password"]
    }
    token_response = api_client.post(reverse('token'), token_data)
    headers = {
        "Authorization": f"Bearer {token_response.data['access']}"
    }

    find_response = api_client.get(reverse('find-partner'), headers=headers)

    assert find_response.status_code == 200
    assert "id" in find_response.data
    assert find_response.data["username"] == most_compatible_user["username"]
    assert find_response.data["gender"] == most_compatible_user["gender"]
    assert find_response.data["email"] == most_compatible_user["email"]
    assert find_response.data["zodiac_sign"] == most_compatible_user["zodiac_sign"]
    assert find_response.data["description"] == most_compatible_user["description"]
    assert "photo" in find_response.data
