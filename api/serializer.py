from rest_framework import serializers
from django.apps import apps

from .signals import user_signed_up
"""
Serializer For User
"""


class UserSerializer(serializers.ModelSerializer):
    UserModel = apps.get_model('login.Users')

    class Meta:
        model = apps.get_model('login.Users')
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True,
                                     'help_text': 'Leave empty if no change needed',
                                     'style': {'input_type': 'password', 'placeholder': 'Password'}}}

    def create(self, validated_data):
        user = self.UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user_signed_up.send(sender=self.__class__, email=user.email)
        return user


class UsersLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


"""
Serializer For Category
"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('catalog.Category')
        fields = ('id', 'category_name', 'category_image')


class UpdateCategorySerializer(serializers.ModelSerializer):
    category_image = serializers.ImageField(required=False)

    class Meta:
        model = apps.get_model('catalog.Category')
        fields = ('category_name', 'category_image')


"""
Serializer For Product
"""


class SupImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('catalog.ProductImage')
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    ProductModel = apps.get_model('catalog.Product')
    ProductImageModel = apps.get_model('catalog.ProductImage')

    images = SupImageProductSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    create_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = apps.get_model('catalog.Product')
        fields = ('id', 'product_name', 'product_image', 'category', 'create_by', 'images', 'upload_images')


class UpdateProductSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(required=False)
    images = SupImageProductSerializer(many=True, read_only=True)

    create_by = serializers.CharField(read_only=True)

    class Meta:
        model = apps.get_model('catalog.Product')
        fields = ('id', 'product_name', 'product_image', 'category', 'create_by', 'images')


class AddImageProductSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
