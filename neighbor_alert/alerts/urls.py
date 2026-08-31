from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CommentDetailView,
    CommentListCreateView,
    CustomTokenObtainPairView,
    EmergencyDetailView,
    EmergencyListCreateView,
    IoTEmergencyTriggerView,
    PostDetailView,
    PostListCreateView,
    ProfileView,
    RegisterView,
    alerts_view,
    community_view,
    dashboard_view,
    home_view,
    login_view,
    logout_view,
    map_view,
    register_view,
)

urlpatterns = [
    # ================= HTML Template UI Routes =================
    path('', home_view, name='home'),
    path('alerts/', alerts_view, name='alerts_page'),
    path('community/', community_view, name='community_page'),
    path('map/', map_view, name='map_page'),
    path('dashboard/', dashboard_view, name='dashboard_page'),
    path('login/', login_view, name='login_page'),
    path('register/', register_view, name='register_page'),
    path('logout/', logout_view, name='logout_page'),

    # ================= REST & Auth APIs =================
    # Auth APIs
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', ProfileView.as_view(), name='auth_profile'),

    # Emergency APIs (iot-trigger কে অবশ্যই <uuid:pk> এর ওপরে রাখতে হবে)
    path('api/emergency/iot-trigger/', IoTEmergencyTriggerView.as_view(), name='iot_trigger'),
    path('api/emergency/', EmergencyListCreateView.as_view(), name='emergency_list'),
    path('api/emergency/<uuid:pk>/', EmergencyDetailView.as_view(), name='emergency_detail'),

    # Community APIs
    path('api/posts/', PostListCreateView.as_view(), name='post_list'),
    path('api/posts/<uuid:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Comment APIs
    path('api/comments/', CommentListCreateView.as_view(), name='comment_list'),
    path('api/comments/<uuid:pk>/', CommentDetailView.as_view(), name='comment_detail'),
]