from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer


from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only = True)
    url = serializers.SerializerMethodField(read_only = True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    owner = UserPublicSerializer(source='user', read_only=True)
    # user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'owner',
            'pk',
            # 'user_id',
            # 'user',
            'title',
            'url',
            'edit_url',
            'content',
            'price',
            'sale_price',
            'discount',
            'public',
        ]

    def get_user(self, obj):
        request = self.context.get('request')
        return request.user.user_name
    
    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('product-detail', kwargs={'pk':obj.pk}, request=request)
    
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('product-update', kwargs={'pk':obj.pk}, request=request)

    def get_discount(self, obj):
        if isinstance(obj, Product):
            return obj.get_discount()
        else:
            return None
        
    def validate_title(self, value):
        request = self.context.get('request')
        user = request.user
        qs = Product.objects.filter(title__iexact = value, user=user)
        print(user, qs)
        if qs.exists():
            raise serializers.ValidationError(f'{value} is already a product name.')
        return value