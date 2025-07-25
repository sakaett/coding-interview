from collections import OrderedDict
from rest_framework import viewsets,response
from api.serializers.company import CompanySerializer
from api.serializers.category import CategorySerializer
from api.models import Company,Category

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(Company.objects.get(id=pk))
        data = serializer.data
        data['categories'] = self._get_categories(data['id'],None)
        return response.Response(data)

    def _get_categories(self,company_id,parent_category_id = None):
        categories = Category.objects.filter(company=company_id,parent_category=parent_category_id)
        # print(categories.query)
        # count()とlen()
        # おそらくcount()はSELECT COUNT(*)、lenはQuerySetのlength
        # lenはすべてのデータを読み込むので、countを推奨する記事が多いが、
        # 複雑なSQLの場合、単一障害点であるDBの負荷になるのでケースバイケースとするべき。
        # 0でない場合にどうせ読み取るならlengthのほうがDBの負荷は少ない。
        if len(categories) == 0:
            return []
        
        result = []
        for data in categories:
            serializer = CategorySerializer(instance=data)
            category_row = serializer.data
            category_row['children'] = self._get_categories(company_id,category_row['id'])
            result.append(category_row)
        return result
    