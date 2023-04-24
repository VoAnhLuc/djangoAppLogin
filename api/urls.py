from django.urls import path, include
from . import views

app_name = 'api'
urlpatterns = [
    # Path for user
    path('users/sign_up', views.CreateUser.as_view(), name='sign_up'),
    path('users/login_create_token', views.LoginCreateToken.as_view(), name='login_create_token'),
    path('users/logout', views.LogoutUser.as_view(), name='logout_user'),
    path('users/refresh_user_token', views.RefreshUserToken.as_view(), name='refresh_user_token'),

    # Path for category
    path('category/', views.ListCreateCategory.as_view(), name='list_create_category'),
    path('category/detail/<int:category_id>', views.DetailCategory.as_view(),
         name='detail_category'),

    # Path for product
    path('product/', views.ListProduct.as_view(), name='list_create_product'),
    path('product/detail/<int:product_id>', views.DetailProduct.as_view(),
         name='detail_product'),

    path('product/detail/<int:product_id>/images', views.ImageProduct.as_view(),
         name='images_product'),
    path('product/detail/<int:product_id>/images/<int:image_id>', views.DeleteImageProduct.as_view(),
         name='images_product'),

    # path('test/', views.TestCelery.as_view(), name='test'),

]
