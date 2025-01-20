from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import TRANSACTION_LOG
from cart_management.models import CART
from api_management.serializers import TransactionSerializer
#to import stripe api modules
from django.conf import settings
import stripe

# Create your views here.
def DisplayPage(request):
    return render(request, 'checkout_template.html')

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

#Checkout method to process user payments using Stripe payment gateway
def checkout(request):
    if request.method == 'POST':
        try:
            amount_in_rands = int(float(request.POST.get('totalPurchaseTotal')))
            print("AMOUNT IN WORDS: ", amount_in_rands)
            amount = amount_in_rands * 100  # Amount in cents (R50.00)(2 decimals)
            currency = 'zar'

            # Create a new charge
            charge = stripe.Charge.create(
                amount=amount,
                currency=currency,
                source=request.POST.get('stripeToken'),  # obtained with Stripe.js
                description='Payment for product',
            )
            print("payment successful")

            # Construct success message
            success_message = f"Your payment of R{amount_in_rands} was successfully processed."

            # Return success response
            return JsonResponse({"success": True, "message": success_message}, status=200)

        except stripe.error.StripeError as e:
            # Handle Stripe errors
            error_message = f"An error occurred while processing your payment: {str(e)}"
            print("Error: ", e)

            # Return error response
            return JsonResponse({"success": False, "error": error_message}, status=400)

        except Exception as e:
            # Catch any other errors
            print("Error: ", e)
            return JsonResponse({"success": False, "error": "An unexpected error occurred."}, status=500)

    # If it's not a POST request, return a JsonResponse saying it's not allowed
    return JsonResponse({"success": False, "error": "Invalid request method. Please use POST."}, status=405)


class CheckoutTrackingView(APIView):
    def get(self, request, transaction_id=None):
        """
        Retrieve transaction logs. If `transaction_id` is provided, retrieves a specific transaction log.
        """
        if transaction_id:
            try:
                transaction = TRANSACTION_LOG.objects.get(id=transaction_id)
                serializer = TransactionSerializer(transaction)
                return JsonResponse({"success": True, "data": serializer.data}, status=200)
            except TRANSACTION_LOG.DoesNotExist:
                return JsonResponse({"success": False, "error": "Transaction not found"}, status=404)

        transactions = TRANSACTION_LOG.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse({"success": True, "data": serializer.data}, status=200, safe=False)

    def post(self, request):
        """
        Create a new transaction log entry when a user checks out.
        The cart data is linked to the transaction.
        """
        cart_id = request.data.get("cartId")
        try:
            cart = CART.objects.get(id=cart_id)
        except CART.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart not found"}, status=404)

        # Create a transaction log from the cart data
        transaction_data = {"cartId": cart.id}
        serializer = TransactionSerializer(data=transaction_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": True, "data": serializer.data}, status=201)
        return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

    def put(self, request, transaction_id):
        """
        Update an existing transaction log.
        """
        try:
            transaction = TRANSACTION_LOG.objects.get(id=transaction_id)
        except TRANSACTION_LOG.DoesNotExist:
            return JsonResponse({"success": False, "error": "Transaction not found"}, status=404)

        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": True, "data": serializer.data}, status=200)
        return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

    def delete(self, request, transaction_id):
        """
        Delete a transaction log.
        """
        try:
            transaction = TRANSACTION_LOG.objects.get(id=transaction_id)
        except TRANSACTION_LOG.DoesNotExist:
            return JsonResponse({"success": False, "error": "Transaction not found"}, status=404)

        transaction.delete()
        return JsonResponse({"success": True, "message": "Transaction deleted successfully"}, status=204)

from django.http import JsonResponse
from checkout_management.models import TRANSACTION_LOG
from cart_management.models import CART
from browse_management.models import MENU
from product_management.models import PRODUCT
from django.contrib.auth.models import User
from api_management.serializers import TransactionSerializer

def add_first_cart_item_to_transaction(request):
    """
    API endpoint to add the first cart item to the transaction log as an entry.
    """

    if request.method == 'GET':
        try:
            # Retrieve the first cart item
            first_cart_item = CART.objects.select_related('menuId', 'menuId__productId', 'userId').first()
            if not first_cart_item:
                return JsonResponse({"success": False, "error": "No items in the cart"}, status=404)

            # Add the cart item to the transaction log
            transaction_data = {"cartId": first_cart_item.id}
            serializer = TransactionSerializer(data=transaction_data)
            if serializer.is_valid():
                serializer.save()

                # Prepare response
                menu_item = first_cart_item.menuId
                product = menu_item.productId
                user = first_cart_item.userId

                response_data = {
                    "transaction": {
                        "transactionId": serializer.instance.id,
                        "cartId": first_cart_item.id,
                    },
                    "cart_item": {
                        "id": first_cart_item.id,
                        "datetimeAdded": first_cart_item.datetimeAdded,
                    },
                    "menu_item": {
                        "id": menu_item.id,
                    },
                    "product": {
                        "id": product.id,
                        "name": product.prodName,
                        "price": product.prodPrice,
                        "description": product.prodDesc,
                        "available_quantity": product.prodAvailQuant,
                        "on_menu": product.prodOnMenu,
                    },
                    "user": {
                        "id": user.id,
                        "username": user.username,
                    },
                }

                return JsonResponse({"success": True, "data": response_data}, status=201)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    if request.method == 'POST':
        try:
            # Retrieve the first cart item
            first_cart_item = CART.objects.select_related('menuId', 'menuId__productId', 'userId').first()
            if not first_cart_item:
                return JsonResponse({"success": False, "error": "No items in the cart"}, status=404)

            # Add the cart item to the transaction log
            transaction_data = {"cartId": first_cart_item.id}
            serializer = TransactionSerializer(data=transaction_data)
            if serializer.is_valid():
                serializer.save()

                # Prepare response
                menu_item = first_cart_item.menuId
                product = menu_item.productId
                user = first_cart_item.userId

                response_data = {
                    "transaction": {
                        "transactionId": serializer.instance.id,
                        "cartId": first_cart_item.id,
                    },
                    "cart_item": {
                        "id": first_cart_item.id,
                        "datetimeAdded": first_cart_item.datetimeAdded,
                    },
                    "menu_item": {
                        "id": menu_item.id,
                    },
                    "product": {
                        "id": product.id,
                        "name": product.prodName,
                        "price": product.prodPrice,
                        "description": product.prodDesc,
                        "available_quantity": product.prodAvailQuant,
                        "on_menu": product.prodOnMenu,
                    },
                    "user": {
                        "id": user.id,
                        "username": user.username,
                    },
                }

                return JsonResponse({"success": True, "data": response_data}, status=201)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)
