from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

# Create your views here.

from orders.forms import GuestCheckoutForm
from orders.models import UserCheckout
from products.models import Variation

from .models import Cart, CartItem


class ItemCountView(View):
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			cart_id = self.request.session.get("cart_id")

			if cart_id == None:
				count = 0 
			else:
				cart = Cart.objects.get(id=cart_id)
				count = cart.items.count()

			request.session["cart_item_count"] = count

			return JsonResponse({"count": count})
		else: 
			raise Http404


class CartView(View):
	model = Cart
	templete_name = "carts/view.html"

	def get_object(self, *args, **kwargs):
		self.request.session.set_expiry(0)   # 300 seconds
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			cart = Cart()
			# self.request.user.get_tax_percentage
			cart.tax_percentage = 0.75
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id

		cart = Cart.objects.get(id=cart_id)

		if self.request.user.is_authenticated():
			cart.user = self.request.user
			cart.save()
		return cart


	def get(self, request, *args, **kwargs):
		cart = self.get_object()

		item_id = request.GET.get("item") 
		
		delete_item = request.GET.get("delete", False)
		flash_message = ""
		item_added = False 

		if item_id: 
			item_instance = get_object_or_404(Variation, id=item_id)
			qty = request.GET.get("qty", 1)
			try:
				if int(qty) < 1:
					delete_item = True
			except:
				raise Http404

			cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
			
			if created:
				item_added = True
				flash_message = "Successfully added to the cart."
			if delete_item:
				flash_message = "Item removed successfully."
				cart_item.delete()  
			else:
				if not created:
					flash_message = "Quantity has been updated successfully."
					cart_item.quantity = qty
					cart_item.save() 

			if not request.is_ajax():
				return HttpResponseRedirect(reverse("cart"))
				# return cart_item.cart.get_absolute_url()
 
		if request.is_ajax():
			try:
				total = cart_item.line_item_total
			except:
				total = None

			try: 
				subtotal = cart_item.cart.subtotal
			except:
				subtotal = None

			try:
				cart_total = cart_item.cart.total
			except:
				cart_total = None

			try:
				tax_total = cart_item.cart.tax_total
			except:
				tax_total = None

			try: 
				total_items = cart_item.cart.items.count()
			except:
				total_items = 0

			data = {
				"deleted": delete_item, 
				"item_added":item_added, 
				"line_total": total,
				"subtotal": subtotal,
				"cart_total": cart_total,
				"tax_total": tax_total,
				"flash_message": flash_message,
				"total_items": total_items,
			}
			return JsonResponse(data)

		context = {
			"object": self.get_object()
		}
		templete = self.templete_name

		return render(request, templete, context)

class CheckoutView(FormMixin, DetailView): 
	model = Cart
	template_name = "carts/checkout_view.html"
	form_class = GuestCheckoutForm

	def get_object(self, *args, **kwargs):
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			return redirect("cart")
		cart = Cart.objects.get(id=cart_id)
		return cart

	def get_context_data(self, *args, **kwargs):
		context = super(CheckoutView, self).get_context_data(*args, **kwargs)
		user_can_continue = False
		user_check_id = self.request.session.get("user_checkout_id")

		if not self.request.user.is_authenticated() or user_check_id == None:  # or if request.user.is_guest:
			context["login_form"] = AuthenticationForm()
			context["next_url"] = self.request.build_absolute_uri()

		elif self.request.user.is_authenticated() or user_check_id != None:	# or if request.user.is_guest:
			user_can_continue = True
		else: 
			pass

		if self.request.user.is_authenticated():
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			self.request.session["user_checkout_id"] = user_checkout.id 

		context["user_can_continue"] = user_can_continue
		context["form"] = self.get_form()
 		return context

 	def post(self, request, *args, **kwargs):
 		self.object = self.get_object()
 		form = self.get_form()
 		if form.is_valid():
 			email = form.cleaned_data.get("email")
 			user_checkout, created = UserCheckout.objects.get_or_create(email=email)
 			request.session["user_checkout_id"] = user_checkout.id
 			return self.form_valid(form)
 		else: 
 			return self.form_invalid(form)

 	def get_success_url(self):
 		return reverse("checkout")


 