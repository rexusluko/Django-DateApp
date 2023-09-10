import pytest
from django.urls import reverse
from date_app.models import ZodiacSign

@pytest.mark.django_db
def test_user(api_client):
    ZodiacSign.objects.create(name="Cancer")

    user_data = {
        "username": "new_boy5",
        "password": "1234",
        "gender": "male",
        "email": "new_boy5@example.com",
        "zodiac_sign": "Cancer",
        "description": "I'm a user",
    }
    create_user_response = api_client.post(reverse('register'), user_data)

    assert create_user_response.status_code == 201
    assert create_user_response.data["username"] == user_data["username"]
    assert create_user_response.data["gender"] == user_data["gender"]
    assert create_user_response.data["email"] == user_data["email"]
    assert create_user_response.data["zodiac_sign"] == user_data["zodiac_sign"]
    assert create_user_response.data["description"] == user_data["description"]