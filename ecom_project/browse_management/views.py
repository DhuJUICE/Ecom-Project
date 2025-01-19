from django.shortcuts import render
from django.http import JsonResponse
from .models import MENU
from product_management.models import PRODUCT
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status

# Create your views here.
def DisplayPage(request):
    return render(request, 'browse_template.html')

#MENU API ENDPOINT
class MenuItemsAPIView(APIView):
    def get(self, request):
        # Step 1: Get all products marked for display
        products_to_display = PRODUCT.objects.filter(prodOnMenu=True)

        # Step 2: Add missing products to the MENU table
        existing_menu_products = set(MENU.objects.values_list('productId', flat=True))
        products_to_add = products_to_display.exclude(id__in=existing_menu_products)
        new_menu_objects = [
            MENU(productId=product)  # Default itemQuantAdded and itemTotal removed
            for product in products_to_add
        ]
        MENU.objects.bulk_create(new_menu_objects)  # Bulk create for efficiency

        # Step 3: Remove products from the MENU table that are no longer marked for display
        product_ids_to_keep = set(products_to_display.values_list('id', flat=True))
        MENU.objects.exclude(productId__id__in=product_ids_to_keep).delete()

        # Step 4: Retrieve the updated MENU items
        menu_items = MENU.objects.select_related('productId')

        # Step 5: Prepare a list of dictionaries for JSON response
        menu_data = [
            {
                'productId': item.productId.id,
                'prodName': item.productId.prodName,
                'prodPrice': float(item.productId.prodPrice),  # Convert Decimal to float for JSON serialization
                'prodDesc': item.productId.prodDesc,
                'prodAvailQuant': item.productId.prodAvailQuant,
            }
            for item in menu_items
        ]

        # Return the JSON response
        return JsonResponse({'menu_items': menu_data}, status=status.HTTP_200_OK, safe=False)

    def put(self, request):
        # Get the data from the PUT request
        data = request.data

        # Ensure we receive a list of items to update
        if not isinstance(data, list):
            return JsonResponse({"message": "Invalid data format. Expected a list of items."}, status=status.HTTP_400_BAD_REQUEST)

        updated_items = []
        for item_data in data:
            product_id = item_data.get('productId')
            if not product_id:
                return JsonResponse({"message": "Missing 'productId' for one of the menu items."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the item exists in the MENU table
            try:
                menu_item = MENU.objects.get(productId_id=product_id)
            except MENU.DoesNotExist:
                raise NotFound(detail=f"Menu item with productId {product_id} not found.")

            # Update the fields as required
            menu_item.productId.prodName = item_data.get('prodName', menu_item.productId.prodName)
            menu_item.productId.prodPrice = item_data.get('prodPrice', menu_item.productId.prodPrice)
            menu_item.productId.prodDesc = item_data.get('prodDesc', menu_item.productId.prodDesc)
            menu_item.productId.prodAvailQuant = item_data.get('prodAvailQuant', menu_item.productId.prodAvailQuant)

            # Save the updated menu item
            menu_item.productId.save()
            updated_items.append({
                'productId': menu_item.productId.id,
                'prodName': menu_item.productId.prodName,
                'prodPrice': float(menu_item.productId.prodPrice),
                'prodDesc': menu_item.productId.prodDesc,
                'prodAvailQuant': menu_item.productId.prodAvailQuant,
            })

        # Return the JSON response with the updated items
        return JsonResponse({'updated_menu_items': updated_items}, status=status.HTTP_200_OK, safe=False)