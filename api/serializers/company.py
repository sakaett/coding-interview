from rest_framework import serializers
from api.models import Company

class CompanySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length = 50,
        required=True,
        error_messages={
            'max_length': '会社名は50文字以内で入力してください。',
            'required': '会社名は必須です。',
            'blank': '会社名を入力してください。',
        }        
    )

    class Meta:
        model = Company
        fields = ('id','name','created_at','updated_at')
        read_only_fields = ('id',)