from django.shortcuts import render

# Create your views here.
def DisplayPage(request):
    return render(request, 'cart_template.html')

from django.http import JsonResponse
from rest_framework.views import APIView
from .models import CART
from browse_management.models import MENU
from django.contrib.auth.models import User
from api_management.serializers import CartSerializer
from django.utils.timezone import now as timezone_now

class CartManagementView(APIView):
    """
    API endpoint for managing the CART model.
    Supports GET, POST, PUT, DELETE.
    """

    def get(self, request, cart_id=None):
        """
        Retrieve cart items with menu and product details, along with the username and userId.
        If `cart_id` is provided, retrieves a specific cart item. Returns a JSON response.
        """
        if cart_id:
            try:
                # Retrieve the specific cart item
                cart_item = CART.objects.get(id=cart_id)

                # Get user details
                user = cart_item.user
                username = user.username if user else "Unknown User"
                user_id = user.id if user else None

                # Retrieve menu and product details
                menu_item = cart_item.menuId
                product = menu_item.productId

                # Prepare the response
                return JsonResponse({
                    "success": True,
                    "data": {
                        "cart_item": {
                            "id": cart_item.id,
                            "datetimeAdded": cart_item.datetimeAdded,
                        },
                        "menu_item": {
                            "id": menu_item.id,
                            "quantity_added": menu_item.itemQuantAdded,
                            "total_price": menu_item.itemTotal,
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
                            "userId": user_id,
                            "username": username,
                        },
                    }
                }, status=200)
            except CART.DoesNotExist:
                return JsonResponse({"success": False, "error": "Cart item not found"}, status=404)

        # Retrieve all cart items
        cart_items = CART.objects.all()
        response_data = []

        for cart_item in cart_items:
            try:
                user = cart_item.userId
                username = user.username if user else "Unknown User"
                user_id = cart_item.userId.id if user else None
                menu_item = cart_item.menuId
                product = menu_item.productId

                response_data.append({
                    "cart_item": {
                        "id": cart_item.id,
                        "datetimeAdded": cart_item.datetimeAdded,
                    },
                    "menu_item": {
                        "id": menu_item.id,
                        "quantity_added": menu_item.itemQuantAdded,
                        "total_price": menu_item.itemTotal,
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
                        "userId": user_id,
                        "username": username,
                    },
                })
            except Exception as e:
                # Handle any unexpected errors gracefully
                response_data.append({"error": str(e)})

        return JsonResponse({"success": True, "data": response_data}, status=200, safe=False)
        
    def post(self, request):
        """
        Create a new cart item.
        Returns JSON response.
        """
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": True, "data": serializer.data}, status=201)
        return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

    def put(self, request, cart_id):
        """
        Update an existing cart item.
        Returns JSON response.
        """
        try:
            cart_item = CART.objects.get(id=cart_id)
        except CART.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart item not found"}, status=404)

        serializer = CartSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": True, "data": serializer.data}, status=200)
        return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

    def delete(self, request, cart_id):
        """
        Delete a cart item.
        Returns JSON response.
        """
        try:
            cart_item = CART.objects.get(id=cart_id)
        except CART.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart item not found"}, status=404)

        cart_item.delete()
        return JsonResponse({"success": True, "message": "Cart item deleted successfully"}, status=204)

#function to test if adding to cart works with first user in User model and first product on the MENu model
class AddToCartQuickView(APIView):
    """
    API endpoint to quickly add the first menu item to the first user’s cart.
    """

    def get(self, request):
        """
        Simulate a POST request to add the first menu item to the first user's cart when visiting the URL.
        Returns JSON response.
        """
        try:
            user = User.objects.first()
            menu_item = MENU.objects.first()

            if not user or not menu_item:
                return JsonResponse({"success": False, "error": "No user or menu item available"}, status=400)

            cart_item = CART.objects.create(
                userId=user.id,
                menuId=menu_item,
                datetimeAdded=timezone_now()
            )

            return JsonResponse({"success": True, "message": "Item added to cart", "cart_id": cart_item.id}, status=201)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def post(self, request):
        """
        Simulate a POST request to add the first menu item to the first user's cart when visiting the URL.
        Returns JSON response.
        """
        try:
            user = request.user
            menu_item = request.POST.get("menu_itemId")

            if not user or not menu_item:
                return JsonResponse({"success": False, "error": "No user or menu item available"}, status=400)

            cart_item = CART.objects.create(
                userId=user.id,
                menuId=menu_item,
                datetimeAdded=timezone_now()
            )

            return JsonResponse({"success": True, "message": "Item added to cart", "cart_id": cart_item.id}, status=201)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)