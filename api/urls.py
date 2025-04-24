from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [

    path('',ApiSummary.as_view(), name="api-summary"),
    path('manage-user/',UserListCreateAPIView.as_view(),name='api-signup'),
    path('manage-user/<int:pk>/',ManageUserAPIView.as_view(),name='manage-user'),
    path('update-user/',UserUpdateAPIView.as_view(),name='update-user'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('change-password/',ChangePasswordAPIView.as_view(),name='change-password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('category/',CategoryListCreateAPIView.as_view(),name='category-list-create'),
    path('category/<slug:slug>/',CategoryDetailUpdateDeleteAPIView.as_view(),name='category-detail-update-delete'),
    path('distributor/',DistributorListCreateAPIView.as_view(),name='distributor-list-create'),
    path('distributor/<slug:slug>/',DistributorDetailUpdateDeleteAPIView.as_view(),name='distributor-detail-update-delete'),
    path('item/',ItemListCreateAPIView.as_view(),name='item-list-create'),
    path('item/<slug:slug>/',ItemDetailUpdateDeleteAPIView.as_view(),name="item-detail-update-delete"),
    path('premises/',ListCreatePremisesAPIView.as_view(),name='list-create-premises'),
    path('premises/<slug:slug>/',PremisesDetailUpdateDeleteAPIView.as_view(),name='detail-update-delete-premises'),
    path('order/',ListCreateOrderAPIView.as_view(),name='list-create-orders'),
    path('order/<slug:slug>/',OrderDetailUpdateDeleteAPIView.as_view(),name='order-update-delete-premises'),
         
]

