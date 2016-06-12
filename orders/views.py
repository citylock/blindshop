from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import AddressForm
from .models import UserAddress

# Create your views here.

class AddressSelectFormView(FormView):
	form_class = AddressForm
	template_name = "orders/address_select.html"


	def get_form(self, *args, **kwargs):
		print "=== LOG IN Function >>> get_form in orders.AddressSelectFormView class"
		form = super(AddressSelectFormView, self).get_form(*args, **kwargs)

		# update queryset ... only shows the address associated with the user
		print form.fields
		form.fields["billing_address"].queryset = UserAddress.objects.filter(
				user__email = self.request.user.email, 
				type='billing',
			)

		form.fields["shipping_address"].queryset = UserAddress.objects.filter(
				user__email = self.request.user.email, 
				type='shipping',
			)

		return form 

	def form_valid(self, form, *args, **kwargs):
		print "=== LOG IN Function >>> form_valid in orders.AddressSelectFormView class"
		print form.cleaned_data["billing_address"].id
		print form.cleaned_data["shipping_address"].id

		billing_address = form.cleaned_data["billing_address"]
		shipping_address = form.cleaned_data["shipping_address"]
		self.request.session["billing_address_id"] = billing_address.id
		self.request.session["shipping_address_id"] = shipping_address.id
		return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

	def get_success_url(self, *args, **kwargs):
		return "/checkout/"
