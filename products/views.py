from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Create your views here.

from .forms import VariationInventoryFormSet
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from .models import Product, Variation, Category


class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "products/product_list.html"

class CategoryDetailView(DetailView):
	model = Category

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = ( product_set | default_products ).distinct()
		context["products"] = products
		return context


 

class VariationListView(StaffRequiredMixin, ListView):
	model = Variation
	
	queryset = Variation.objects.all()
	# queryset = Product.objects.filter(active=False)   # only show deactivated items.. 

	def get_context_data(self, *args, **kwargs):
	 	context = super(VariationListView, self).get_context_data(*args, **kwargs)
	 	context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = Variation.objects.filter(product=product)

		return queryset

	def post(self, request, *args, **kwargs):
		# 
		formset = VariationInventoryFormSet(request.POST, request.FILES)

		# print request.POST
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				if new_item.title:
					product_pk = self.kwargs.get("pk")
					product = get_object_or_404(Product, pk=product_pk)
					new_item.product = product
					new_item.save()

			messages.success(request, "Your inventory and pricing have beeen updated")
			return redirect("products")
		raise Http404





class ProductListView(ListView):
	model = Product
	
	queryset = Product.objects.all()
	# queryset = Product.objects.filter(active=False)   # only show deactivated items.. 

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)

		# can add more context values here, for example
		context["now"] = timezone.now()
		context["query"] = timezone.now()
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query: 
			# standard query format.. for one item to search
			# qs = self.model.objects.filter(title__icontains=query)

			# search for text
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)

			try: 
				# search for decimal
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs|qs2).distinct()
			except:
				pass
		return qs 


import random

class ProductDetailView(DetailView):
	model = Product 
	# templatename = "product.html"
	# template_name = "<appname>/<modelname>_detail.html"
	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		# order_by("-title")
		context["related"] = sorted(Product.objects.get_related(instance)[:4], key= lambda x: random.random())
		return context


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