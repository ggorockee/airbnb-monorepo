from rest_framework.viewsets import ModelViewSet
from .models import Category
from .seirializers import CategorySerializer


class CategoryViewSet(ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
