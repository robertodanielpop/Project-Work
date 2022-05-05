from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class SubscribeAPIView(generics.CreateAPIView):
    queryset = Email.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        else:
            information = User.objects.filter(user_id=user)
            return information

class BasketViewSet(viewsets.ModelViewSet):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()


    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Basket.objects.all()
        else:
            shopping_basket = Basket.objects.filter(user_id=user, is_active=True)
            return shopping_basket

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        else:
            orders = Order.objects.filter(user_id=user)
            return orders

class AddBasketItemAPIView(generics.CreateAPIView):
    serializer_class = AddBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItems.objects.all()

class RemoveBasketItemAPIView(generics.CreateAPIView):
    serializer_class = RemoveBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItems.objects.all()

class DeleteBasketItemAPIView(generics.CreateAPIView):
    serializer_class = DeleteBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItems.objects.all()

class CheckoutAPIView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    queryset = APIUser.objects.all()

class DeleteUserAPIView(generics.CreateAPIView):
    serializer_class = DeleteUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = APIUser.objects.all()

    def delete(self, request, * args, ** kwargs):
        user_account = self.request.user
        user_account.delete()

        return Response({"action": "account has been deleted"})

class ChangeUserPasswordAPIView(generics.CreateAPIView):
    serializer_class = ChangeUserPasswordSerializer
    permission_classes = [IsAuthenticated]
    queryset = APIUser.objects.all()

    def update(self, request, *args, ** kwargs):
        user_password_serializer = self.get_serializer(data=request.user)
        user_password = serializer.save()

        if hasattr(user_password, 'auth_token'):
            user_password.auth_token.delete()
            token, created = Token.objects.get_or_create(user_password)

        return Response({"action": "Password Changed"})