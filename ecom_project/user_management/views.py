from django.shortcuts import render

# Create your views here.
def DisplayPage(request):
	return render(request, 'user_template.html')