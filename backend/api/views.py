import json
from django.http import JsonResponse

from products.models import Product


def api_home(request, *args, **kwaargs):

    # body = request.body  # Byte string of JSON data
    # print(request.GET)  # url query params
    # data = {}

    # try:
    #     data = json.loads(body)
    # except:
    #     pass

    # print(data)
    # data['params'] = dict(request.GET)
    # data['headers'] = dict(request.headers)  # request.META ->
    # print(request.headers)
    # data['content_type'] = request.content_type  # 

    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price

    return JsonResponse(data)
