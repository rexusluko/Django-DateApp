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
    new_user = create_user_response.data['user']

    assert create_user_response.status_code == 201
    assert new_user["username"] == user_data["username"]
    assert new_user["gender"] == user_data["gender"]
    assert new_user["email"] == user_data["email"]
    assert new_user["zodiac_sign"] == user_data["zodiac_sign"]
    assert new_user["description"] == user_data["description"]
    assert 'access' in create_user_response.data
