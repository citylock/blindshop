from django import forms


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
			return email2
		else: 
			print 'Fail: checkout emails are NOT the same'
			raise forms.ValidationError("Please confirm emails are the same")