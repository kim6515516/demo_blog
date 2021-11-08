from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.paginations import StandardResultsSetPagination
from api.serializers import ArticleCommonSerializer, CommentCommonSerializer, CommentUpdateSerializer
from article.models import Article, Comment


class ArticleApiView(GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         ):

    queryset = Article.objects.prefetch_related('comments').all()

    serializer_class = ArticleCommonSerializer
    pagination_class = StandardResultsSetPagination


class ArticleCommentApiView(GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         ):

    queryset = Comment.objects.all()

    serializer_class = CommentCommonSerializer
    pagination_class = StandardResultsSetPagination

    # lookup_field = 'comment_pk'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_action_classes = {
            # 'list': CommentListSerializer,
            'create': CommentUpdateSerializer,
            # 'retrieve': CommentSerializer,
            'update': CommentUpdateSerializer,
            # 'partial_update': CommentSerializer,
            # 'destroy': CommentSerializer,
        }

    def get_serializer_class(self, *args, **kwargs):
        """Instantiate the list of serializers per action from class attribute (must be defined)."""
        kwargs['partial'] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs.get('article_pk'):
            queryset = queryset.filter(article=self.kwargs['article_pk'])

        if self.kwargs.get('pk'):
            queryset = queryset.filter(id=self.kwargs['pk'])

        return queryset

    def create(self, request, *args, **kwargs):
        article_pk = kwargs['article_pk']
        request.data.update({'article': int(article_pk)})
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        super().perform_create(serializer)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)