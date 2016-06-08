from django import forms
from django.contrib.auth import get_user_model
from .models import UserCheckout

User = get_user_model()

class GuestCheckoutForm(forms.Form):
	print "LOG IN - GuestCheckoutForm in order.forms"
	email = forms.EmailField()
	email2 = forms.EmailField(label='Verify Email')

	def clean_email2(self):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")

		print email 
		print email2

		if email == email2:
			print 'Success: checkout emails are the same'
			# fixed : It does not work with get_user_model, so use UserCheckout instead
			# user_exists = User.objects.filter(email=email).count()
			user_exists = UserCheckout.objects.all().filter(email=email).count()
			# print num_acc
			print "Number of user account : %d" % user_exists
			if user_exists != 0:
				raise forms.ValidationError("This User already exists. Please login instead.")

			return email2
		else: 
			print 'Fail: checkout emails are NOT the same'
			raise forms.ValidationError("Please confirm emails are the same")