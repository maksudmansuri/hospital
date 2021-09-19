


from django.db.models.fields import DecimalField
# from front.context_processors import basket
# from front.models import Product
from decimal import Decimal


class Basket():
    """
        Checkout session stored
    """

    def __init__(self,request):
        self.session = request.session
        basket =self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] ={}
        self.basket = basket 

    def add(self,order):
        order_id=order.id
        if order_id not in self.basket:
            self.basket[order_id] = {'order_id':order.id}

        self.session.modified =True
    
    def __id__(self):
        """
        get order id from here"""
        order_id = self.basket.key('order_id')
        return self.basket[order_id]['order_id']
   

    
    def delete(self,product):
        """
        Delete Item for session data
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
        
        self.save()


    def save(self):
        self.session.modified =True
