from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.events.models import Category
from apps.events.serializers import CategorySerializer


@api_view(["GET"])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
