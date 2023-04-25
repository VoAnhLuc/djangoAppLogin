from django.contrib.auth import authenticate, login as auth_login, logout
from rest_framework import generics, status, views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import (UserSerializer, UsersLoginSerializer,
                         CategorySerializer, UpdateCategorySerializer,
                         ProductSerializer, UpdateProductSerializer,
                         AddImageProductSerializer
                         )
from django.apps import apps
from drf_yasg.utils import swagger_auto_schema
from .tasks import hello
"""
API for User
"""


class CreateUser(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    UserModel = apps.get_model('login.Users')
    queryset = UserModel.objects.order_by('-date_joined')[:5]

    @swagger_auto_schema(operation_summary='Get 5 user lastest')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ConfirmEmail(views.APIView):
    UserModel = apps.get_model('login.Users')

    def get(self, request, email, *args, **kwargs):
        try:
            user = self.UserModel.objects.get(email=email)
        except self.UserModel.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user.is_staff = True
            user.save()
            return Response({'message': 'Active user success'}, status=status.HTTP_200_OK)


class LoginCreateToken(generics.GenericAPIView):
    serializer_class = UsersLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                auth_login(request, user)
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(views.APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = {
            'user': str(request.user),
            'message': 'Logout Success',
            }
        logout(request)

        return Response(data, status=status.HTTP_200_OK)


class RefreshUserToken(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        refresh = RefreshToken.for_user(request.user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)


"""
API for Category
"""


class ListCreateCategory(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    CategoryModel = apps.get_model('catalog.Category')
    queryset = CategoryModel.objects.all()

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DetailCategory(generics.GenericAPIView):
    serializer_class = UpdateCategorySerializer
    CategoryModel = apps.get_model('catalog.Category')

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id, *args, **kwargs):
        category = self.CategoryModel.objects.get(id=category_id)
        serializer = self.serializer_class(category)
        return Response(serializer.data)

    def put(self, request, category_id, *args, **kwargs):
        category = self.CategoryModel.objects.get(id=category_id)
        serializer = self.serializer_class(data=request.data, instance=category)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, category_id, *args, **kwargs):
        category = self.CategoryModel.objects.get(id=category_id)
        selected_product = category.product_set.filter(category=category_id)

        if selected_product:
            data = {'message': 'Have a product in category, Cant delete!'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)

        else:
            category.delete()
            data = {'message': 'Delete Category Success'}
            return Response(data, status=status.HTTP_202_ACCEPTED)


"""
API for Product
"""


class ListProduct(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    ProductModel = apps.get_model('catalog.Product')
    ProductImageModel = apps.get_model('catalog.ProductImage')
    queryset = ProductModel.objects.all()

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        upload_images = data.pop('upload_images')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        for image in upload_images:
            self.ProductImageModel.objects.create(product=product, image=image)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DetailProduct(generics.GenericAPIView):
    serializer_class = UpdateProductSerializer
    ProductModel = apps.get_model('catalog.Product')

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id, *args, **kwargs):
        product = self.ProductModel.objects.get(id=product_id)
        serializer = self.serializer_class(product)
        return Response(serializer.data)

    def put(self, request, product_id, *args, **kwargs):
        product = self.ProductModel.objects.get(id=product_id)
        serializer = self.serializer_class(data=request.data, instance=product)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, product_id, *args, **kwargs):
        product = self.ProductModel.objects.get(id=product_id)
        product.delete()
        data = {'message': 'Delete Category Success'}
        return Response(data, status=status.HTTP_202_ACCEPTED)


class ImageProduct(generics.GenericAPIView):
    ProductModel = apps.get_model('catalog.Product')
    ProductImageModel = apps.get_model('catalog.ProductImage')

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = AddImageProductSerializer

    def get(self, request, product_id, *args, **kwargs):
        product = self.ProductModel.objects.get(id=product_id)
        images = self.ProductImageModel.objects.filter(product_id=product_id).values()
        all_image = []
        for image in images:
            all_image.append(image)

        data = {
            'product': product.product_name,
            'images': all_image
        }
        return Response(data)

    def post(self, request, product_id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            images = serializer.validated_data['images']
            for image in images:
                self.ProductImageModel.objects.create(product_id=product_id, image=image)

            data = {
                'message': 'add new image success',
            }
            return Response(data)

        return Response(serializer.data, status=status.HTTP_304_NOT_MODIFIED)


class DeleteImageProduct(generics.GenericAPIView):
    ProductImageModel = apps.get_model('catalog.ProductImage')
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, image_id, *args, **kwargs):
        image = self.ProductImageModel.objects.get(id=image_id)
        image.delete()
        data = {'message': 'Delete Image Success'}
        return Response(data, status=status.HTTP_202_ACCEPTED)


class TestCelery(views.APIView):

    def get(self, request, *args, **kwargs):
        a = hello.delay()
        data = {'message': a.get()}
        return Response(data, status=status.HTTP_202_ACCEPTED)
