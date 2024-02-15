import json

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.forms.models import model_to_dict

from products.models import Product

from products.serializers import ProductSerializer

@api_view(["POST"])
def api_home(request, *args, **kwaargs):

    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        # print(instance)
        print(serializer.data)
        return Response(serializer.data)
    
    return Response({'invalid':'not good data'}, status=400)
