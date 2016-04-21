from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Product

class ProductListView(ListView):
	model = Product
	

class ProductDetailView(DetailView):
	model = Product 
	# templatename = "product.html"
	# template_name = "<appname>/<modelname>_detail.html"


def product_detail_view_func(request,id):
	# Method 1
	# product_instance = Product.objects.get(id=id)

	# Method 2
	product_instance = get_object_or_404(Product, id=id)

	# Method 3
	try:
		product_instance = Product.object.get(id=id)
	except Product.DoesNotExist: 
		raise Http404
	except: 
		raise Http404


	template = "products/product_detail.html"
	context = {
		"object": product_instance
	}

	return render(request, template, context)