from django.shortcuts import render
from django.http import JsonResponse
from .models import MENU
from product_management.models import PRODUCT

# Create your views here.
def DisplayPage(request):
	return render(request, 'browse_template.html')

#function to get the menu items to be displayed on the MENU
def get_menu_items(request):
    # Step 1: Get all products marked for display
    products_to_display = PRODUCT.objects.filter(prodOnMenu=True)

    # Step 2: Add missing products to the MENU table
    existing_menu_products = set(MENU.objects.values_list('productId', flat=True))
    products_to_add = products_to_display.exclude(id__in=existing_menu_products)
    new_menu_objects = [
        MENU(productId=product, itemQuantAdded=0, itemTotal=0)  # Default itemQuantAdded and itemTotal
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
            'itemQuantAdded': item.itemQuantAdded,
            'itemTotal': float(item.itemTotal),  # Convert Decimal to float
        }
        for item in menu_items
    ]

    # Return the JSON response
    return JsonResponse({'menu_items': menu_data}, safe=False)