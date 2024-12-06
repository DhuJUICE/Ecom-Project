from django.shortcuts import render

# Create your views here.
def LoginPage(request):
	return render(request, 'login.html')

def SignUpPage(request):
	return render(request, 'sign_up.html')