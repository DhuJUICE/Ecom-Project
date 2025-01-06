from django.shortcuts import render

# Create your views here.
def DisplayPage(request):
	return render(request, 'checkout_template.html')

#to import stripe api modules
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def checkout(request):
    if request.method == 'POST':
        amount_in_rands = int(float(request.POST.get('totalPurchaseTotal')))
        print("AMOUNT IN WORDS: ", amount_in_rands)
        amount = amount_in_rands*100 # Amount in cents (R50.00)(2decimals)
        currency = 'zar'

        try:
            # Create a new charge
            charge = stripe.Charge.create(
                amount=amount,
                currency=currency,
                source=request.POST.get('stripeToken'),  # obtained with Stripe.js
                description='Payment for product',
            )
            print("payment successful")
            return render(request, 'home.html')
        except stripe.error.StripeError as e:
            print("Error: ", e)

    return render(request, 'checkout.html', {'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY, 'amount_in_rands':amount_in_rands})
