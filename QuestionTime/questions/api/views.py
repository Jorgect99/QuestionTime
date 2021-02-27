from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from questions.api.permissions import IsAuthorOrReadOnly
from questions.api.serializers import QuestionSerializer, AnswerSerializer
from questions.models import Question, Answer

class QuestionViewSet(viewsets.ModelViewSet):
    
    queryset = Question.objects.all()
    lookup_field = "slug"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class AnswerCreateAPIView(generics.CreateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)

        if question.answers.filter(author = request_user).exists():
            raise ValidationError("You  have already answered this question.")

        serializer.save(author = request_user, question = question)


class AnswerListAPIView(generics.ListAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug = kwarg_slug).order_by("-created_at")


class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
     
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

class AnswerLikeAPIView(APIView):

    serializer_class = AnswerSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk = pk)
        user = request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(answer, context = serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):

        answer = get_object_or_404(Answer, pk = pk)
        user = request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(answer, context = serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

