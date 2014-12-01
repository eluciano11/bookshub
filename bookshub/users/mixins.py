from djstripe.models import Customer


class CustomerMixin(object):
    def get_customer(self):
        try:
            return self.request.user.customer
        except:
            return Customer.create(self.request.user)
