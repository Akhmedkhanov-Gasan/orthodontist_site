import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import AboutPage, HomePage, Work


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_home_page_returns_404_when_home_page_does_not_exist(api_client):
    response = api_client.get(reverse("home-page"))

    assert response.status_code == 404
    assert response.data == {"detail": "Not found."}


@pytest.mark.django_db
def test_get_home_page_returns_home_page(api_client):
    HomePage.objects.create(
        hero_title="Главный заголовок",
        hero_subtitle="Описание главного блока",
        about_title="О клинике",
        about_text="Текст о клинике",
    )

    response = api_client.get(reverse("home-page"))

    assert response.status_code == 200
    assert response.data["hero_title"] == "Главный заголовок"
    assert response.data["hero_subtitle"] == "Описание главного блока"
    assert response.data["about_title"] == "О клинике"
    assert response.data["about_text"] == "Текст о клинике"


@pytest.mark.django_db
def test_get_about_page_returns_404_when_about_page_does_not_exist(api_client):
    response = api_client.get(reverse("about-page"))

    assert response.status_code == 404
    assert response.data == {"detail": "Not found."}


@pytest.mark.django_db
def test_get_about_page_returns_about_page(api_client):
    AboutPage.objects.create(
        title="О нас",
        content="Описание клиники",
    )

    response = api_client.get(reverse("about-page"))

    assert response.status_code == 200
    assert response.data["title"] == "О нас"
    assert response.data["content"] == "Описание клиники"


@pytest.mark.django_db
def test_get_works_returns_empty_list_when_no_works_exist(api_client):
    response = api_client.get(reverse("works-list"))

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_get_works_returns_work_list(api_client):
    Work.objects.create(
        title="До и после",
        description="Описание работы",
    )

    response = api_client.get(reverse("works-list"))

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "До и после"
    assert response.data[0]["description"] == "Описание работы"