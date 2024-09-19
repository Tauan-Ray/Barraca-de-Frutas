from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Fruits


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')
            else:
                return redirect('seller')
        else:
            errors = form.errors
    else:
        form = AuthenticationForm()
        errors = None
    
    return render(request, 'login.html', {'form': form, 'errors': errors})


@login_required
def seller_site(request):
    fruits = Fruits.objects.all()
    return render(request, 'seller.html', {'fruits': fruits})


@login_required
def list_fruits(request):
    term = request.GET.get('term', '')
    fruits = Fruits.objects.filter(name__icontains=term)
    results = [{
        'id': fruit.id,
        'label': fruit.name,
        'value': fruit.name,
        'classification': fruit.get_classification_display(),
        'fresh_fruits': fruit.get_fresh_fruits_display(),
        'price': fruit.price
    } for fruit in fruits]
    return JsonResponse(results, safe=False)


@login_required
def search_fruit(request):
    if request.method == 'POST':
        name = request.POST.get('fruit')
        classification = request.POST.get('classification')
        fresh = request.POST.get('fresh')
    
        fruits = Fruits.objects.all()
        
        if name:
            fruits = fruits.filter(name__icontains=name)
        
        if classification:
            fruits = fruits.filter(classification=classification)
        
        if fresh:
            if fresh.lower() in ['sim', 's', '1', 'true']:
                fresh_value = 'Y'
            elif fresh.lower() in ['não', 'n', '0', 'false']:
                fresh_value = 'N'
            else:
                fresh_value = None

            if fresh_value:
                fruits = fruits.filter(fresh_fruits=fresh_value)
            

        return render(request, 'seller.html', {'fruits': fruits})
    

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')