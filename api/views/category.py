from rest_framework import generics,response
from api.serializers.category import CategorySerializer
from api.models import Category

class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryView(generics.UpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self,request,pk):
        serializer = self.get_serializer(Category.objects.get(id=pk))
        return response.Response(serializer.data)


    def delete(self,request,pk):
        Category.objects.get(id=pk).delete()
        return response.Response('{}',status=204)


        
