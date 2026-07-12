from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer,UserSerializer,RegisterSerializer
from rest_framework import generics,permissions
from django.contrib.auth.models import User
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class UserPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "size"
    max_page_size = 20
class UsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    filter_backends = [
    DjangoFilterBackend,
    SearchFilter,
    OrderingFilter,
]
    
    filterset_fields = ["is_active", "is_staff","username"]
    ordering_fields = ["username", "date_joined"]
    search_fields = ["username", "email"]
    pagination_class = UserPagination

class LoginView(APIView):

    permission_classes = []

    authentication_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({

            "access": str(refresh.access_token),
            "refresh": str(refresh),

            "user": {
                "id": user.id,
                "username": user.username,
            }

        })
    from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes=[]

    def post(self, request):

        refresh = request.data["refresh"]

        token = RefreshToken(refresh)
        token.blacklist()

        return Response({
            "message": "Logout successful"
        })


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "Registration successful.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
            

    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    

# class UserDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes=[IsAuthenticated,permissions.IsAdminUser]
#     serializer_class=UserSerializer
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#     def put(self, request, *args, **kwargs):
#         return super().put(request, *args, **kwargs)
#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)