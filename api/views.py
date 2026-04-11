from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Category, Blog, Comment, FAQ, Tag
from .serializers import (
    UserSerializer, RegisterSerializer, CategorySerializer, 
    BlogSerializer, CommentSerializer, FAQSerializer, TagSerializer
)
from .ai_grammar import grammar_ai
from .chatbot import get_chatbot_response
from .permissions import IsAuthorOrAdmin

# Authentication Views
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Blog & Category Views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(status='published')
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAuthorOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        tag = self.request.query_params.get('tag')
        if category:
            queryset = queryset.filter(category__slug=category)
        if tag:
            queryset = queryset.filter(tags__name__iexact=tag) | queryset.filter(tags__slug=tag)
        return queryset.distinct()

class UserBlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrAdmin)
    lookup_field = 'slug'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.all()
        blog_slug = self.request.query_params.get('blog')
        if blog_slug:
            queryset = queryset.filter(blog__slug=blog_slug)
        return queryset

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        return [permissions.AllowAny()]

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = (permissions.AllowAny,)

class FAQChatbotView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        query = request.data.get('query', '')
        if not query:
            return Response({'error': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Use grammar AI to clean the query before processing
        corrected_query, _ = grammar_ai.suggest_correction(query)
        
        # Get response using TF-IDF logic (from filtered/corrected query)
        answer = get_chatbot_response(corrected_query)
        
        return Response({
            'query': query,
            'corrected_query': corrected_query,
            'answer': answer
        })

class AIGrammarCheckView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Now returns both corrected text and a list of changes
        corrected_text, changes = grammar_ai.suggest_correction(text)
        
        return Response({
            'original': text,
            'corrected': corrected_text,
            'changes': changes
        })

