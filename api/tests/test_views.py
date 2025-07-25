from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Company
from api.models import Category

class CompanyViewTests(APITestCase):
    def setUp(self):
        pass

    # createのテスト
    def test_create(self):
        # company作成
        response = self.client.post('/api/companies/',{'name': 'company_0'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(),1)
        self.assertEqual(Company.objects.last().name,'company_0')


        #categoryをcompanyの配下に作成
        response = self.client.post('/api/categories/',{'company':Company.objects.last().id,
                                                        'name':'category1'
                                                        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(),1)
        self.assertEqual(Category.objects.last().name,'category1')


    # post系のvalidationのテスト
    def test_validate_post(self):

        # companyのチェック
        # name length
        x_name = ""
        for i in range(0,51,1):
            x_name += "あ"
        response = self.client.post('/api/companies/',{'name': x_name})
        errors = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(errors['name'][0],'会社名は50文字以内で入力してください。')

        # name blank
        response = self.client.post('/api/companies/',{'name': ''})
        errors = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(errors['name'][0],'会社名を入力してください。')

        # name required
        response = self.client.post('/api/companies/',{})
        errors = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(errors['name'][0],'会社名は必須です。')


        # categoryのチェック

        # company not found
        response = self.client.post('/api/companies/',{'name': 'test'})
        company_id = Company.objects.last().id
        response = self.client.delete(f'/api/companies/{company_id}/')

        response = self.client.post('/api/categories/',{'company':company_id,
                                                        'name':'category1'
                                                        })
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(errors['company'][0],'指定された会社は存在しません。')

        # company required
        response = self.client.post('/api/categories/',{
                                                        'name':'category1'
                                                        })
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(errors['company'][0],'会社は必須です。')

        # company null
        response = self.client.post('/api/categories/',{'company':'',
                                                        'name':'category1'
                                                        })
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(errors['company'][0],'company.idを入力してください。')

        # name length
        response = self.client.post('/api/companies/',{'name': 'test'})
        company_id = Company.objects.last().id

        response = self.client.post('/api/companies/',{'name': 'test2'})
        # レコードが複数ある場合ス、last()は不定?または非同期処理?
        # 確実にidを取るなら以下
        other_company_id = response.json()['id']

        x_name = ""
        for i in range(0,51,1):
            x_name += "あ"
        response = self.client.post('/api/categories/',{'company':company_id,
                                                        'name':f'{x_name}'
                                                        })
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(errors['name'][0],'カテゴリ名は30文字以内で入力してください。')

        # name blank
        response = self.client.post('/api/categories/',{'company':company_id,
                                                        'name':''
                                                        })
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(errors['name'][0],'カテゴリ名を入力してください。')

        # name required
        response = self.client.post('/api/categories/',{'company':company_id,
                                                        })
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(errors['name'][0],'カテゴリ名は必須です。')

        # parent_category が無い
        response = self.client.post('/api/categories/',{'company':company_id,
                                                        'name':'parent_category'
                                                        })
        parent_category_id = Category.objects.last().id

        response = self.client.post('/api/categories/',{'company':other_company_id,
                                                        'name':'other_parent_category'
                                                        })
        other_category_id = response.json()['id']
    

        response = self.client.delete(f'/api/categories/{parent_category_id}')

        response = self.client.post('/api/categories/',{'company':company_id,
                                                        'name':'name1',
                                                        'parent_category':parent_category_id
                                                        })
        self.assertEqual(response.status_code, 400)        
        errors = response.json()
        self.assertEqual(errors['parent_category'][0],'指定されたカテゴリは存在しません。')

        # parent_categoryの会社と自分の会社が異なる
        response = self.client.post('/api/categories/',{'company':company_id,
                                                        'name':'name1',
                                                        'parent_category':other_category_id
                                                        })
        self.assertEqual(response.status_code, 400)        
        errors = response.json()
        self.assertEqual(errors['non_field_errors'][0],'指定された親カテゴリの会社と自分の会社が異なります。')


    # 更新系のvalidateのテスト
    def test_validate_patch(self):
        response = self.client.post('/api/companies/',{'name': 'comp1'})
        comp1_id = response.json()['id']
        response = self.client.post('/api/companies/',{'name': 'comp2'})
        comp2_id = response.json()['id']

        response = self.client.post('/api/categories/',{'company':comp1_id,
                                                        'name':'cate1',
                                                        })
        cate1_id = response.json()['id']

        response = self.client.post('/api/categories/',{'company':comp1_id,
                                                        'name':'cate1_2',
                                                        'parent_category': cate1_id
                                                        })
        cate1_2_id = response.json()['id']

        response = self.client.post('/api/categories/',{'company':comp2_id,
                                                        'name':'cate2',
                                                        })
        cate2_id = response.json()['id']

        response = self.client.post('/api/categories/',{'company':comp2_id,
                                                        'name':'cate3',
                                                        })
        cate3_id = response.json()['id']

        # company name length
        x_name = ""
        for i in range(0,51,1):
            x_name += "あ"
        response = self.client.patch(f'/api/companies/{comp1_id}/',{'name':f'{x_name}'})
        self.assertEqual(response.status_code, 400)        
        errors = response.json()
        self.assertEqual(errors['name'][0],'会社名は50文字以内で入力してください。')

        # company name blank
        response = self.client.patch(f'/api/companies/{comp1_id}/',{'name':''})
        self.assertEqual(response.status_code, 400)        
        errors = response.json()
        self.assertEqual(errors['name'][0],'会社名を入力してください。')

        # company name required。patchでは部分更新である事の確認
        response = self.client.patch(f'/api/companies/{comp1_id}/',{})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'],'comp1')

        x_name = ""
        for i in range(0,51,1):
            x_name += "あ"
        response = self.client.patch(f'/api/categories/{cate1_id}',{
                                                        'name':f'{x_name}'
                                                        })
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(errors['name'][0],'カテゴリ名は30文字以内で入力してください。')

        # name blank
        response = self.client.patch(f'/api/categories/{cate1_2_id}',{
                                                        'name':''
                                                        })
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertEqual(errors['name'][0],'カテゴリ名を入力してください。')

        # name required patchで部分更新なので200
        response = self.client.patch(f'/api/categories/{cate2_id}',{
                                                        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'],'cate2')

        # parent_category が無い
        response = self.client.delete(f'/api/categories/{cate3_id}')

        response = self.client.patch(f'/api/categories/{cate1_2_id}',{
                                                        'parent_category':cate3_id
                                                        })
        self.assertEqual(response.status_code, 400)        
        errors = response.json()
        self.assertEqual(errors['parent_category'][0],'指定されたカテゴリは存在しません。')

        # parent_categoryの会社と自分の会社が異なる
        response = self.client.patch(f'/api/categories/{cate1_2_id}',{
                                                        'parent_category':cate2_id
                                                        })
        errors = response.json()
        self.assertEqual(response.status_code, 400)        
        self.assertEqual(errors['non_field_errors'][0],'指定された親カテゴリの会社と自分の会社が異なります。')


    def test_list(self):
        # company
        response = self.client.post('/api/companies/',{'name': 'company_1'})
        comp1_id = response.json()['id']
        response = self.client.post('/api/companies/',{'name': 'company_2'})
        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        #category
        response = self.client.post('/api/categories/',{'company':comp1_id,
                                                        'name':'cate1',
                                                        })
        response = self.client.post('/api/categories/',{'company':comp1_id,
                                                        'name':'cate2',
                                                        })
        response = self.client.post('/api/categories/',{'company':comp1_id,
                                                        'name':'cate3',
                                                        })
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)



    def test_retrieve(self):
        # category
        response = self.client.post('/api/companies/',{'name': 'company_0'})
        company_0_id = response.json()['id']
        response = self.client.post('/api/categories/',{'company':company_0_id,
                                                        'name':'category1'
                                                        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category1_id = response.data['id']

        response = self.client.post('/api/categories/',{'company':company_0_id,
                                                        'parent_category': category1_id,
                                                        'name':'category2',
                                                        })
        category2_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/api/categories/',{'company':company_0_id,
                                                        'parent_category': category1_id,
                                                        'name':'category3',
                                                        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/api/categories/',{'company':company_0_id,
                                                        'parent_category': category2_id,
                                                        'name':'category2_2',
                                                        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # categoryのGET
        response = self.client.get(f'/api/categories/{category1_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'],'category1')

        # companyのGET
        # companyを取得した場合、所属するカテゴリをtreeで取得したい
        response = self.client.get(f'/api/companies/{company_0_id}/')
        # とりあえず子の数だけチェック
        self.assertEqual( len(response.data['categories']),1)
        self.assertEqual( len(response.data['categories'][0]['children']),2)
        self.assertEqual( len(response.data['categories'][0]['children'][0]['children']),1)

    def test_update(self):
        # company
        response = self.client.post('/api/companies/',{'name': 'company_1'})
        response = self.client.post('/api/companies/',{'name': 'company_3'})
        response = self.client.get('/api/companies/')
        # response.dataはOrderdDict
        id = response.data[0]['id']

        response = self.client.patch(f'/api/companies/{id}/',{'name': 'company_2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f'/api/companies/{id}/')
        # response.dataは連想配列
        #print(response.json())
        self.assertEqual(response.data['name'],'company_2')

        # category
        response = self.client.post('/api/categories/',{'company':id,
                                                        'name':'category1'
                                                        })
        category1_id = response.json()['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/api/categories/',{'company':id,
                                                        'name':'category2'
                                                        })
        category2_id = response.json()['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update category1
        response = self.client.patch(f'/api/categories/{category1_id}',{
                                                        'name':'category1 UPDATE'
                                                        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'],'category1 UPDATE')    

        # update category2 parentをcategory1に
        response = self.client.patch(f'/api/categories/{category2_id}',{
                                                        'name':'category2 UPDATE',
                                                        'parent_category': category1_id
                                                        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'],'category2 UPDATE')    


    def test_destroy(self):
        # company
        response = self.client.post('/api/companies/',{'name': 'company_1'})
        response = self.client.get('/api/companies/')
        id = response.data[0]['id']
        response = self.client.delete(f'/api/companies/{id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # category
        company1 = Company.objects.create(name='parent company')
        category1 = Category.objects.create(company=company1,name="cate 1")        
        category2 = Category.objects.create(company=company1,name="cate 2",parent_category=category1)
        response = self.client.delete(f'/api/companies/{company1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # exceptionのチェック
        with self.assertRaises(Category.DoesNotExist):
            category_chk1 = Category.objects.get(id=category1.id)
        with self.assertRaises(Category.DoesNotExist):
            category_chk2 = Category.objects.get(id=category2.id)

