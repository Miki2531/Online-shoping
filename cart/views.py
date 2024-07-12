from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, 
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial= {
            'quantity': item['quantity'],
            'override': True
        })
        coupon_apply_form = CouponApplyForm()
        
        r = Recommender()
        cart_prodcuts = [item['product'] for item in cart]
        if(cart_prodcuts):
            recommender_products = r.suggest_products_for(
                cart_prodcuts, max_results=4
            )
        else:
            recommender_products = []
    return render(request, 'cart/detail.html', 
                  {'cart': cart, 'coupon_apply_form' : coupon_apply_form,
                   'recommender_products': recommender_products}
                  )


