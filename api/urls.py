from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views.company import CompanyViewSet
from .views.category import CategoryListView,CategoryView

router = DefaultRouter()
router.register('companies',CompanyViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path('categories/',CategoryListView.as_view()),
    path('categories/<uuid:pk>',CategoryView.as_view()),
    ]
