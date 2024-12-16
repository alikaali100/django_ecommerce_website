from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, DiscountViewSet, ProductFeatureViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'discounts', DiscountViewSet, basename='discount')
router.register(r'product-features', ProductFeatureViewSet, basename='product-feature')

urlpatterns = router.urls
