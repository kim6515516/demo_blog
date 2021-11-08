from rest_framework import serializers

from article.models import Article, Comment


class CommentCommonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content')
        read_only_fields = ('id', )
        write_only_fields = ('content',)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content', 'article')
        read_only_fields = ('id', )
        write_only_fields = ('content',)


class ArticleCommonSerializer(serializers.ModelSerializer):

    comments = CommentCommonSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'comments')
        read_only_fields = ('id', 'comments')
        write_only_fields = ('title', 'content')

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
