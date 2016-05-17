from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import SingleObjectMixin

# Create your views here.

from products.models import Variation
from carts.models import Cart, CartItem


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
				total_items = cart_item.cart.items.count()
			except:
				total_items = 0

			data = {
				"deleted": delete_item, 
				"item_added":item_added, 
				"line_total": total,
				"subtotal": subtotal,
				"flash_message": flash_message,
				"total_items": total_items,
			}
			return JsonResponse(data)

		context = {
			"object": self.get_object()
		}
		templete = self.templete_name

		return render(request, templete, context)
