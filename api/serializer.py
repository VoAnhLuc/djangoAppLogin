from rest_framework import serializers
from django.apps import apps


"""
Serializer For User
"""


class UserSerializer(serializers.ModelSerializer):
    UserModel = apps.get_model('login.Users')

    class Meta:
        model = apps.get_model('login.Users')
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = self.UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class UsersLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


class CategoryForm(serializers.ModelSerializer):
    """Form for the category model"""
    class Meta:
        model = apps.get_model('catalog.Category')
        fields = ('category_name', 'category_image')
