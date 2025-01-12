from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Order, DiscountCode, OrderItem
from product.models import Product
from customers.models import Customer, Address
from .serializers import CartItemSerializer, OrderSerializer
from django.utils import timezone

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
    
class CartAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please log in to view your cart."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        customer = request.user
        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get all cart items for the user
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response(
            {"cart_items": serializer.data},
            status=status.HTTP_200_OK,
        )

class RemoveFromCartAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please log in to remove items from your cart."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        customer = request.user
        product_id = request.data.get('product')  # product ID to be removed from cart

        # Validate product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve cart for the customer
        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Find the cart item to remove
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Item not found in cart."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the cart item
        cart_item.delete()

        return Response(
            {"detail": "Item removed from cart successfully."},
            status=status.HTTP_200_OK,
        )
    
class UpdateCartItemAPIView(APIView):
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please log in to update items in your cart."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        customer = request.user
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')

        if quantity is None or quantity <= 0:
            return Response(
                {"detail": "Quantity must be greater than zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve or create cart for the customer
        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Find the cart item to update
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Item not found in cart."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update the quantity
        cart_item.quantity = quantity
        cart_item.save()

        return Response(
            {"detail": "Item quantity updated successfully."},
            status=status.HTTP_200_OK,
        )
    
class CheckoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please log in to proceed with checkout."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        customer = request.user

        # Retrieve the cart for the user
        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "No cart found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve all items in the cart and calculate total price
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response(
                {"detail": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_price = sum([item.product.price * item.quantity for item in cart_items])

        # Get discount code if provided
        discount_code = request.data.get('discount_code')
        discount_amount = 0

        if discount_code:
            try:
                discount = DiscountCode.objects.get(code=discount_code)
                if discount.start_date > timezone.now() or discount.end_date < timezone.now():
                    return Response(
                        {"detail": "Discount code is expired."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if discount.usage_limit <= 0:
                    return Response(
                        {"detail": "Discount code has been used up."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
                # Apply discount based on type
                if discount.type == 'PG':  # Percentage discount
                    discount_amount = total_price * discount.amount / 100
                elif discount.type == 'FA':  # Fixed Amount discount
                    discount_amount = discount.amount

                # Ensure the discount doesn't exceed the max allowed amount
                if discount.max_amount and discount_amount > discount.max_amount:
                    discount_amount = discount.max_amount

                # Update the usage limit of the discount
                discount.usage_limit -= 1
                discount.save()

            except DiscountCode.DoesNotExist:
                return Response(
                    {"detail": "Invalid discount code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Calculate the final amount after discount
        final_amount = total_price - discount_amount
        if final_amount < 0:
            final_amount = 0  # Ensure final amount is not negative

        # Check if the address is valid or create a new one if not provided
        address_id = request.data.get('address')
        address = None

        if address_id:
            # Try to get the address if it's already saved
            try:
                address = Address.objects.get(id=address_id, customer=customer)
            except Address.DoesNotExist:
                return Response(
                    {"detail": "Invalid or non-existent address."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # If no address is provided, create a new address
            new_address_data = request.data.get('new_address')
            if new_address_data:
                # Create a new Address object using the provided data
                address = Address.objects.create(
                    customer=customer,
                    province=new_address_data.get('province'),
                    city=new_address_data.get('city'),
                    detailed_address=new_address_data.get('detailed_address')
                )
            else:
                return Response(
                    {"detail": "Address is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Create order
        order = Order.objects.create(
            customer=customer,
            address=address,
            discount_code=discount if discount_code else None,
            total_amount=final_amount
        )

        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                discount_amount=cart_item.product.price * cart_item.quantity - (cart_item.product.price * cart_item.quantity - final_amount)
            )

        # Clear the cart after checkout
        cart_items.delete()

        return Response(
            {"detail": f"Order {order.id} placed successfully. Total amount: {final_amount}."},
            status=status.HTTP_200_OK,
        )

class OrderListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please log in to view your orders."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        customer = request.user  

        orders = Order.objects.filter(customer=customer).order_by('-created_at')

        if not orders.exists():
            return Response(
                {"detail": "You have no orders."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)