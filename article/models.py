from django.db import models

# Create your models here.
from django.utils.timezone import now


class SoftDeleteManager(models.Manager):
    use_for_related_fields = True  # 옵션은 기본 매니저로 이 매니저를 정의한 모델이 있을 때 이 모델을 가리키는 모든 관계 참조에서 모델 매니저를 사용할 수 있도록 한다.

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):

    deleted_at = models.DateTimeField('삭제일', null=True, default=None)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('업데이트일', auto_now=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save(update_fields=['deleted_at'])

    def restore(self):  # 삭제된 레코드를 복구한다.
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])


class Article(models.Model):
    title = models.CharField(verbose_name='제목', max_length=255)
    content = models.TextField(verbose_name='내용')

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(verbose_name='내용', max_length=255)

    class Meta:
        ordering = ['-id']




