from rest_framework import serializers
from api.models import Category,Company
from api.serializers.company import CompanySerializer

class CategorySerializer(serializers.ModelSerializer):

    def validate(self,attrs):
        # parent_categoryがある場合
        if ('parent_category' in attrs) and attrs['parent_category'] is not None:
            # attrs['parent_category]はオブジェクトが入る
            # 各項目のvalidate( company = など)が先に実行されるようである
            parent_category = None
            try:
                parent_category = Category.objects.get(id=attrs['parent_category'].id)
            except Category.DoesNotExist:
                # これはdead code
                raise serializers.ValidationError('指定された親カテゴリは存在しません。2')
            # 存在する場合、自分と親カテゴリで会社が同じかどうか
            if ('company' in attrs ) and parent_category.company.id != attrs['company'].id:
                raise serializers.ValidationError('指定された親カテゴリの会社と自分の会社が異なります。')
            elif self.instance is not None and parent_category.company.id != self.instance.company.id:
                raise serializers.ValidationError('指定された親カテゴリの会社と自分の会社が異なります。')
            if self.instance is not None:
                # 自分が他のカテゴリの子になる場合、ループしないようにする必要がある
                if self.instance.id == attrs['parent_category'].id:
                    raise serializers.ValidationError('自分は親カテゴリに指定できません。')
            if self.instance is not None and self.instance.parent_category is None:
                # 自分が他のカテゴリの子になる場合、ループしないようにする必要がある
                childCategories = Category.objects.filter(parent_category=self.instance.id)
                if childCategories.count() > 0:
                    raise serializers.ValidationError('自分は親カテゴリなので、他のカテゴリの子に指定できません。')


        return attrs


    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required = True,
        error_messages={
            'does_not_exist': '指定された会社は存在しません。',
            'incorrect_type': 'companyにはuuidを指定してください。',
            'required': '会社は必須です。',
            'null': 'company.idを入力してください。',
        }
    )

    parent_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required = False,
        allow_null = True,
        error_messages={
            'does_not_exist': '指定されたカテゴリは存在しません。',
            'incorrect_type': 'parent_categoryにはuuidを指定してください。',
        }
    )
    
    name = serializers.CharField(
        required = True,
        max_length = 30,
        error_messages={
            'max_length': 'カテゴリ名は30文字以内で入力してください。',
            'required': 'カテゴリ名は必須です。',
            'blank': 'カテゴリ名を入力してください。',
        }  

    )
        
    class Meta:
        model = Category
        fields = ('id','company','name','parent_category','created_at','updated_at')
        read_only_fields = ('id',)

