from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from api import customauthentication, custompermissions
from favourites.custompermissions import AllowOnlyOwner
from favourites.models import Favourite
from restaurants.models import Restaurant
from foods.models import Food
from restaurants.serializers import RestaurantSerializer
from foods.serializers import FoodSerializer


class FoodFavourite(APIView):
    permission_classes = [
        IsAuthenticated,
        custompermissions.AllowOnlyCustomer,
        AllowOnlyOwner,
    ]
    authentication_classes = [
        TokenAuthentication,
        customauthentication.CsrfExemptSessionAuthentication
    ]

    def get(self, request, pk):
        customer = self.request.user.customer
        try:
            content_object = Food.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": "No food item with that id exists."
                }, 
                status=HTTP_404_NOT_FOUND
            )
        content_type = ContentType.objects.get_for_model(content_object)
        try:
            fav = Favourite.objects.get(
                customer=customer, 
                content_type=content_type, 
                object_id=content_object.id
            )
            fav.delete()
            return Response(
                {
                    "success": "Food removed from customer's favourite."
                }, 
                status=HTTP_200_OK
            )
        except ObjectDoesNotExist:
            fav = Favourite.objects.create(customer=customer, content_object=content_object)
            return Response(
                {
                    "success": "Food added to customer's favourite."
                }, 
                status=HTTP_201_CREATED
            )


class RestaurantFavourite(APIView):
    permission_classes = [
        IsAuthenticated,
        custompermissions.AllowOnlyCustomer,
        AllowOnlyOwner,
    ]
    authentication_classes = [
        TokenAuthentication,
        customauthentication.CsrfExemptSessionAuthentication
    ]

    def get(self, request, pk):
        customer = self.request.user.customer
        try:
            content_object = Restaurant.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": "No restaurant item with that id exists."
                }, 
                status=HTTP_404_NOT_FOUND
            )
        content_type = ContentType.objects.get_for_model(content_object)
        try:
            fav = Favourite.objects.get(
                customer=customer, 
                content_type=content_type, 
                object_id=content_object.id
            )
            fav.delete()
            return Response(
                {
                    "success": "Restaurant removed from customer's favourite."
                }, 
                status=HTTP_200_OK
            )
        except ObjectDoesNotExist:
            fav = Favourite.objects.create(customer=customer, content_object=content_object)
            return Response(
                {
                    "success": "Restaurant added to customer's favourite."
                }, 
                status=HTTP_201_CREATED
            )


class MyFavourites(APIView):
    permission_classes = [
        IsAuthenticated,
        custompermissions.AllowOnlyCustomer,
        AllowOnlyOwner,
    ]
    authentication_classes = [
        TokenAuthentication,
        customauthentication.CsrfExemptSessionAuthentication
    ]

    def get(self, request):
        customer = self.request.user.customer
        items = customer.favourite
        restaurant_favs = items.filter(content_type__id=11)
        food_favs = items.filter(content_type__id=12)
        foods = [f.content_object for f in food_favs]
        restaurants = [r.content_object for r in restaurant_favs]
        
        if foods or restaurants:
            return Response({
                "foods": FoodSerializer(instance=foods, many=True, context={'request': request}).data,
                "restaurants": RestaurantSerializer(instance=restaurants, many=True, context={'request': request}).data
            }, status=HTTP_200_OK)
        else:
            return Response({
                "error": "You have not bookmarked any foods or restaurants"
            }, status=HTTP_404_NOT_FOUND)
        