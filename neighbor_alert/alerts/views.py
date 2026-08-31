from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Comment, Emergency, Post
from .serializers import (
    CommentSerializer,
    EmergencySerializer,
    PostSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


# ================= UI Views =================
def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def alerts_view(request):
    return render(request, 'alert.html')


@login_required
def community_view(request):
    return render(request, 'community.html')


@login_required
def map_view(request):
    return render(request, 'map.html')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


# ================= API Views =================
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class EmergencyListCreateView(generics.ListCreateAPIView):
    queryset = Emergency.objects.all().order_by('-created_at')
    serializer_class = EmergencySerializer

    def perform_create(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(
                    username='anonymous_user', password='password123'
                )
        serializer.save(user=user)


class EmergencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer


class IoTEmergencyTriggerView(APIView):
    def post(self, request):
        data = request.data
        default_user = User.objects.first()
        if not default_user:
            default_user = User.objects.create_user(
                username='iot_device', password='password123'
            )

        alert = Emergency.objects.create(
            user=default_user,
            type=data.get('type', 'Fire'),
            title=data.get('title', 'IoT Sensor Emergency Alert'),
            description=data.get(
                'description', 'Abnormal conditions detected by IoT sensor.'
            ),
            location=data.get('location', 'Sensor Location'),
            severity=data.get('severity', 'High'),
            status='Pending',
            is_iot_triggered=True,
        )
        serializer = EmergencySerializer(alert)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(
                    username='anonymous_user', password='password123'
                )
        serializer.save(user=user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# ================= Comment API Views =================
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(
                    username='anonymous_user', password='password123'
                )
        serializer.save(user=user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer