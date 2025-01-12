from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from product.models import Product
from customers.models import Customer

class AddToCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please log in to add items to your cart."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        customer = request.user
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        # Validate product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve or create cart for the customer
        cart, _ = Cart.objects.get_or_create(customer=customer)

        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response(
            {"detail": "Item added to cart successfully."},
            status=status.HTTP_200_OK,
        )
