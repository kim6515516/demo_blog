from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from api.views import ArticleApiView, ArticleCommentApiView

app_name = "api"

router = SimpleRouter(trailing_slash=False)
router.register(r'articles', ArticleApiView)

articles_router = routers.NestedSimpleRouter(router, r'articles', lookup='article')
articles_router.register(r'comments', ArticleCommentApiView, basename='article-comment')

urlpatterns = []
#
urlpatterns += router.urls
urlpatterns += articles_router.urls
