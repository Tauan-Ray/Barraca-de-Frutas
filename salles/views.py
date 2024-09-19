from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Fruits, Sales, Order
from django.utils import timezone


@login_required
def sale_page(request):
    error = None
    if request.method == 'POST':
        fruit_names = request.POST.getlist('fruit_name[]')
        quantities = request.POST.getlist('quantity_number[]')
        total_text = request.POST.get('total_purchase')
        discount = request.POST.get('discount')


        for fruit in fruit_names:
            fruits = Fruits.objects.filter(name__icontains=fruit)
            if not fruits:
                error = f'{fruit} não é uma fruta registrada. Insira apenas nomes de frutas existentes'
                return render(request, 'page_sale.html', {'error': error})
                
        index = total_text.index(':')

        total = total_text[index+2:]

        fruit_names = [name for name in fruit_names if name.strip()]
        quantities = [qty for qty in quantities if qty.strip()]

        if not fruit_names:
            pass
        
        else:
            order = Order.objects.create(seller=request.user)
            
            for fruit_name, quantity in zip(fruit_names, quantities):
                all_fruit = get_object_or_404(Fruits, name=fruit_name)

                if all_fruit.stock >= int(quantity):
                    fruit_price = float(all_fruit.price)
                    quantity = int(quantity)
                    total_price = fruit_price * quantity

                    value_discount = (int(discount)/100) * total_price
                    new_value = total_price - value_discount

                    
                    sale = Sales(
                        order=order,
                        fruit=all_fruit,
                        quantity=quantity,
                        fruit_price=fruit_price,
                        discount=int(discount),
                        total_price=new_value
                    )
                    sale.save()

                    order.total_purchase = float(total)
                    order.save()
                    
                    all_fruit.stock -= quantity
                    all_fruit.save()

                else:
                    error = f'Estoque insuficiente para {fruit_name}. Quantidade solicitada: {quantity}, Estoque disponível: {all_fruit.stock}'

                    return render(request, 'page_sale.html', {'error': error})


    return render(request, 'page_sale.html', {'error': error})


@login_required
def show_order(request):
    seller = request.user

    sales = Sales.objects.filter(order__seller=seller).order_by('-order__sale_time')
    orders = Order.objects.filter(seller=seller)

    total = sum(order.total_purchase for order in orders)

    sales_data = []
    for sale in sales:
        sale_time_local = timezone.localtime(sale.order.sale_time)
        sales_data.append({
            'fruit_name': sale.fruit,
            'fruit_price': sale.fruit_price,
            'quantity': sale.quantity,
            'total_price': sale.total_price,
            'discount': sale.discount,
            'sale_time': sale_time_local.strftime('%d-%m-%Y | %H:%M:%S')
        })

    return render(request, 'order.html', {'sales': sales_data, 'total': total})

    
