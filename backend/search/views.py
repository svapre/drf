from rest_framework.response import Response
from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer

from . import algolia_client


class SearchListView(generics.ListAPIView):
    def get(self, request, *args, **kwaargs):
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        query = request.GET.get('q')
        # print(request.GET.get('public'))
        public = str(request.GET.get('public')) !='0'
        # print(query, user, public)
        if not query:
            return Response('', status=400)
        results = algolia_client.perform_search(query=query, user=user, public=public)
        return Response(results)

class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = None
            # print(self.request.user)
            if self.request.user.is_authenticated:
                user = self.request.user
            
            results = qs.search(q, user=user)
        return results