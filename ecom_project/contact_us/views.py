from django.shortcuts import render
from .models import CONTACT_US
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json


@csrf_exempt
def contact_us(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')

            # Handle the data (save it, send email, etc.)
            # For example, you can save it in your database:
            CONTACT_US.objects.create(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)

            return JsonResponse({'status': 'success', 'message': 'Thank you for contacting us!'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)