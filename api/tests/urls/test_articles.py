import pytest
from django.test import Client

from article.models import Article


def create_mock_article() -> None:
    """
    Article 모델 더미데이터 생성
    :return:
    """
    article: Article = Article()
    article.title = "test_title"
    article.content = "http://www.naaaa.com"
    article.save()


@pytest.mark.django_db
def test_ArticleApiView_GET() -> None:
    """
    ArticleApiView 뷰의 url method GET 테스트 할 수 있다.
    :return:
    """

    # Given
    create_mock_article()

    client = Client()

    # When
    response = client.get('/api/v1/articles')

    # Then
    assert response.status_code == 200
    assert response.context_data["results"].first().title == "test_title"
