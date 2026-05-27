from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Medicine, Category, Symptom, Order, OrderItem
from .cart import Cart
from .forms import CartAddForm, OrderCreateForm, SymptomSearchForm


def home(request):
    """Головна сторінка."""
    categories = Category.objects.all()
    featured = Medicine.objects.filter(is_available=True).order_by('-created')[:8]
    prescription_count = Medicine.objects.filter(is_prescription=True, is_available=True).count()
    otc_count = Medicine.objects.filter(is_prescription=False, is_available=True).count()
    context = {
        'categories': categories,
        'featured': featured,
        'prescription_count': prescription_count,
        'otc_count': otc_count,
    }
    return render(request, 'shop/home.html', context)


def catalog(request):
    """Каталог ліків з фільтрацією."""
    medicines = Medicine.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Фільтри
    category_slug = request.GET.get('category')
    prescription_filter = request.GET.get('prescription')
    search_query = request.GET.get('q', '').strip()
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        medicines = medicines.filter(category=current_category)

    if prescription_filter == 'yes':
        medicines = medicines.filter(is_prescription=True)
    elif prescription_filter == 'no':
        medicines = medicines.filter(is_prescription=False)

    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(composition__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )

    context = {
        'medicines': medicines,
        'categories': categories,
        'current_category': current_category,
        'prescription_filter': prescription_filter,
        'search_query': search_query,
        'total_count': medicines.count(),
    }
    return render(request, 'shop/catalog.html', context)


def medicine_detail(request, slug):
    """Деталі конкретного препарату."""
    medicine = get_object_or_404(Medicine, slug=slug, is_available=True)
    related = Medicine.objects.filter(
        category=medicine.category, is_available=True
    ).exclude(id=medicine.id)[:4]
    cart_form = CartAddForm()
    context = {
        'medicine': medicine,
        'related': related,
        'cart_form': cart_form,
    }
    return render(request, 'shop/medicine_detail.html', context)


def symptom_search(request):
    """Пошук ліків за симптомами."""
    form = SymptomSearchForm(request.GET or None)
    results = []
    all_symptoms = Symptom.objects.all()
    selected_symptom = None
    query = ''

    symptom_slug = request.GET.get('symptom')
    if symptom_slug:
        selected_symptom = get_object_or_404(Symptom, slug=symptom_slug)
        results = Medicine.objects.filter(
            symptoms=selected_symptom, is_available=True
        )
    elif form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = Medicine.objects.filter(
                Q(symptoms__name__icontains=query) |
                Q(name__icontains=query) |
                Q(description__icontains=query),
                is_available=True
            ).distinct()

    context = {
        'form': form,
        'results': results,
        'all_symptoms': all_symptoms,
        'selected_symptom': selected_symptom,
        'query': query,
    }
    return render(request, 'shop/symptom_search.html', context)


def cart_detail(request):
    """Перегляд кошика."""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddForm(
            initial={'quantity': item['quantity'], 'override': True}
        )
    context = {'cart': cart}
    return render(request, 'shop/cart.html', context)


def cart_add(request, medicine_id):
    """Додавання товару до кошика."""
    cart = Cart(request)
    medicine = get_object_or_404(Medicine, id=medicine_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            medicine=medicine,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
        messages.success(request, f'«{medicine.name}» додано до кошика.')
    return redirect('shop:cart_detail')


def cart_remove(request, medicine_id):
    """Видалення товару з кошика."""
    cart = Cart(request)
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart.remove(medicine)
    messages.info(request, f'«{medicine.name}» видалено з кошика.')
    return redirect('shop:cart_detail')


def order_create(request):
    """Оформлення замовлення."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Кошик порожній.')
        return redirect('shop:catalog')

    has_prescription_items = cart.has_prescription_items()

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Перевірка рецепту
            if has_prescription_items and not form.cleaned_data.get('has_prescription'):
                messages.error(
                    request,
                    'У вашому кошику є рецептурні препарати. '
                    'Будь ласка, підтвердьте наявність рецепту.'
                )
            else:
                order = form.save(commit=False)
                order.total_price = cart.get_total_price()
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        medicine=item['medicine'],
                        price=item['price'],
                        quantity=item['quantity'],
                    )
                cart.clear()
                return render(request, 'shop/order_success.html', {'order': order})
    else:
        form = OrderCreateForm()

    context = {
        'cart': cart,
        'form': form,
        'has_prescription_items': has_prescription_items,
    }
    return render(request, 'shop/checkout.html', context)
