"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time

def format_order(product, cart_id):
    """
    Function that formats the product given as input to the wanted string output

    :type product: Product
    :param product: the product to be formated to string

    :type cart_id: int
    :param cart_id: the id of the consumers's cart
    """
    order = "cons{} bought {}".format(cart_id, product)
    return order

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.operations = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        cart_id = self.marketplace.new_cart()
        for j in self.operations:           # j represents the list of commands for each consumer
            for i in j:
                if i['type'] == 'add':
                    while self.marketplace.add_to_cart(cart_id, i) is False:
                        time.sleep(self.retry_wait_time)
                elif i['type'] == 'remove':
                    while self.marketplace.remove_from_cart(cart_id, i) is False:
                        time.sleep(self.retry_wait_time)

        buy_list = self.marketplace.place_order(cart_id)
        for i in buy_list:
            print(format_order(i, cart_id))
