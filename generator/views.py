from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import GeneratePromptRequestSerializer
from .models import generate_image_prompt
import threading
import uuid
from django.core.cache import cache


@api_view(['POST'])
def generate_prompt(request):
    serializer = GeneratePromptRequestSerializer(data=request.data)

    if serializer.is_valid():
        lyrics = serializer.validated_data['lyrics']
        genres = serializer.validated_data['genres']
        mood = serializer.validated_data['mood']

        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Start generation in background thread
        thread = threading.Thread(
            target=generate_image_prompt,
            args=(lyrics, genres, mood),
            kwargs={'request_id': request_id}
        )
        thread.start()

        return Response({
            'request_id': request_id,
            'status': 'started',
            'message': 'Generation started. Use the request_id to check status.'
        }, status=status.HTTP_202_ACCEPTED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_status(request, request_id):
    status = cache.get(f'generation_status_{request_id}')

    if not status:
        return Response({
            'error': 'Request not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if status == 'completed':
        result = cache.get(f'generation_result_{request_id}')
        return Response({
            'status': status,
            'result': result
        })
    elif status == 'error':
        error = cache.get(f'generation_error_{request_id}')
        return Response({
            'status': status,
            'error': error
        })
    else:
        return Response({
            'status': status
        })