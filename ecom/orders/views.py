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
            {"detail": "این محصول با موفقیت به سبد خرید اضافه شد"},
            status=status.HTTP_200_OK,
        )
    
from django.utils.timezone import now

class CartAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please log in to view your cart."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response(
                {"detail": "Your cart is empty."},
                status=status.HTTP_404_NOT_FOUND,
            )

        total_price = 0
        total_quantity = 0

        cart_data = []
        for item in cart_items:
            product = item.product
            discounted_price = product.discounted_price
            total_price += discounted_price * item.quantity
            total_quantity += item.quantity  

            cart_data.append({
                "product_id":product.id,
                "product_name": product.name,
                "quantity": item.quantity,
                "product_price": product.price,
                "discounted_price": discounted_price,
            })

        cart.total_price = total_price
        cart.save()

        return Response(
            {
                "cart_items": cart_data,
                "total_price": total_price,
                "total_quantity": total_quantity,
            },
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
        product_id = request.data.get('product')  

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

        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        total_price = cart.total_price 
        discount_code = request.data.get('discount_code')
        print(discount_code)
        discount_amount = 0

        if discount_code:
            try:
                discount = DiscountCode.objects.get(code=discount_code)
                print(discount)
                print(discount_code)
                current_time = timezone.now()
                if discount.start_date > current_time or discount.end_date < current_time:
                    return Response(
                        {"detail": "Discount code is expired."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if discount.usage_limit <= 0:
                    return Response(
                        {"detail": "Discount code has been used up."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if discount.type == 'PG':  
                    discount_amount = total_price * discount.amount / 100
                elif discount.type == 'FA': 
                    discount_amount = discount.amount
                if discount.max_amount:
                    discount_amount = min(discount_amount, discount.max_amount)

                discount.usage_limit -= 1
                discount.save()

            except DiscountCode.DoesNotExist:
                return Response(
                    {"detail": "Invalid discount code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        final_price = max(total_price - discount_amount, 0)
        # Handle address
        customer = request.user
        address_id = request.data.get('address')
        address = None
        discount = None

        if address_id:
            try:
                address = Address.objects.get(id=address_id, customer=customer)
            except Address.DoesNotExist:
                return Response(
                    {"detail": "Invalid or non-existent address."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            new_address_data = request.data.get('new_address')
            if new_address_data:
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
            discount_code=discount,
            total_amount=final_price  
        )
        # Retrieve cart and create order items
        cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            item_discount_amount = cart_item.product.price * cart_item.quantity - cart_item.product.discounted_price * cart_item.quantity
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                discount_amount=item_discount_amount  
            )

        # Clear the cart
        cart_items.delete()

        return Response(
            {"detail": f"Order placed successfully. Final price: {final_price}."},
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