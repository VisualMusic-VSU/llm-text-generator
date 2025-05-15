from rest_framework import serializers

class GeneratePromptRequestSerializer(serializers.Serializer):
    lyrics = serializers.CharField()
    genres = serializers.ListField(child=serializers.CharField())
    mood = serializers.CharField()