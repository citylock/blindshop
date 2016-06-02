from django.conf import settings
from django.db import models

# Create your models here.

class GuestCheckout(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)   # optional 
	email = models.EmailField()  	# --> required
	#merchant_id

	def __unicode__(self): # def __str__(self):
		return self.email


# class Order(models.Model):
# 	# cart
# 	# user checkout --> required
# 	# guest not required
# 	# shipping address
# 	# billing address
# 	# shipping total price
# 	# order total (cart total + shipping)
# 	# order_id -> custom id 

