from rest_framework import serializers
from .models import *
from rest_framework import generics
import base64
import hashlib
import secrets

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'product_image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_id', 'email', 'first_name', 'last_name', 'telephone', 'address', 'zipcode', 'country', 'city', 'county', 'company', 'address_line']

    def create(self, validated_data):
        user_id = validated_data['user_id']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        telephone = validated_data['telephone']
        address = validated_data['address']
        zipcode = validated_data['zipcode']
        country = validated_data['country']
        city = validated_data['city']
        county = validated_data['county']
        company = validated_data['company']
        address_line = validated_data['address_line']

        request = self.context.get('request', None)
        if request:
            current_user = request.user
            user_details = User.objects.filter(user_id=current_user).first()

            if user_details:

                user_details.email = email
                user_details.first_name = first_name
                user_details.last_name = last_name
                user_details.telephone = telephone
                user_details.address = address
                user_details.zipcode = zipcode
                user_details.country = country
                user_details.city = city
                user_details.county = county
                user_details.company = company
                user_details.address_line = address_line

                user_details.save()
                return user_details

class DeleteUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APIUser
        fields = []

    def create(self, validated_data):
        username = validated_data['username']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            user_details = APIUser.objects.filter(username=username).first()
            if user_details:
                user_details.delete()
        else:
            return None


class UserRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APIUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']
        #address = validated_data['address']
        new_user = APIUser.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        new_basket = Basket.objects.create(user_id = new_user)
        new_basket.save()
        new_user_details = User.objects.create(user_id = new_user)
        new_user_details.save()
        return new_user

class BasketItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BasketItems
        fields = ['product_id', 'product_name', 'quantity', 'item_price']

class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True, source='basketitems_set')

    class Meta:
        model = Basket
        fields = ['id', 'user_id', 'is_active', 'items']

class AddBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItems
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_basket = Basket.objects.filter(user_id=current_user, is_active=True).first()

            basket_items = BasketItems.objects.filter(basket_id=shopping_basket, product_id=product_id).first()
            if basket_items:
                if quantity == 1:
                    basket_items.quantity = basket_items.quantity + 1
                    basket_items.save()
                    print(basket_items.basket_id)
                    return basket_items
                else:
                    basket_items.quantity = basket_items.quantity + quantity
                    basket_items.save()
                    print(basket_items.basket_id)
                    return basket_items
            else:
                new_basket_item = BasketItems.objects.create(basket_id = shopping_basket, product_id=product_id, quantity=quantity)
                new_basket_item.save()

                return new_basket_item
        else:
            return None

class RemoveBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItems
        fields = ['product_id']

    def create(self, validated_data):
        product_id = validated_data['product_id']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_basket = Basket.objects.filter(user_id=current_user, is_active=True).first()
            basket_items = BasketItems.objects.filter(product_id=product_id).first()
            if basket_items:
                if basket_items.quantity > 1:
                    basket_items.quantity = basket_items.quantity - 1
                    basket_items.save()
                    return basket_items
                else:
                    basket_items.delete()

            else:
                return BasketItems.objects.create(basket_id=shopping_basket, product_id=product_id, quantity=0)
        else:
            return None

class DeleteBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItems
        fields = ['product_id']

    def create(self, validated_data):
        product_id = validated_data['product_id']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_basket = Basket.objects.filter(user_id=current_user, is_active=True).first()
            basket_items = BasketItems.objects.filter(product_id=product_id).first()
            if basket_items:
                BasketItems.objects.filter(product_id=product_id).first().delete()
                basket_items.save()
        else:
            return None

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['basket_id', 'total_price']

    def create(self, validated_data):
        request = self.context.get('request', None)
        current_user = request.user
        total_price = validated_data['total_price']
        basket_id = validated_data['basket_id']
        basket_id.is_active = False
        basket_id.save()
        order = Order.objects.create(basket_id=basket_id, user_id=current_user, total_price=total_price)
        order.save()
        new_basket = Basket.objects.create(user_id = current_user)
        new_basket.save()
        return order

class OrderSerializer(serializers.ModelSerializer):
    basket = BasketSerializer(many=True, read_only=True, source='basket_set')

    class Meta:
        model = Order
        fields = ['id', 'basket_id', 'date_ordered', 'user_id', 'basket', 'total_price']

class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ['email']

class ChangeUserPasswordSerializer(serializers.HyperlinkedModelSerializer):
    old = serializers.CharField(write_only=True, required=True)
    new = serializers.CharField(write_only=True, required=True)
    new2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = APIUser
        fields = ['old', 'new', 'new2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        request = self.context.get('request', None)
        old = validated_data['old']
        new = validated_data['new']
        new2 = validated_data['new2']

        if request:
            current_user = request.user
            print(current_user)
            user_details = APIUser.objects.filter(username=current_user).first()
            print(user_details.password)


            if user_details:
                if user_details.check_password(validated_data['old']):
                    if new == new2:
                        user_details.set_password(validated_data['new'])
                        user_details.save()
                        raise serializers.ValidationError({'new': 'Password changed'})
                    else:
                        raise serializers.ValidationError({'new': 'Passwords not matching'})
                else:
                    raise serializers.ValidationError({'old': 'Current Password Incorrect'})
            return user_details
        else:
            return None