from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import GeneratePromptRequestSerializer
from .model import generate_image_prompt


@api_view(['POST'])
def generate_prompt(request):
    serializer = GeneratePromptRequestSerializer(data=request.data)

    if serializer.is_valid():
        lyrics = serializer.validated_data['lyrics']
        genres = serializer.validated_data['genres']
        mood = serializer.validated_data['mood']

        try:
            generated_prompt = generate_image_prompt(lyrics, genres, mood)
            return Response({'generated_prompt': generated_prompt}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
