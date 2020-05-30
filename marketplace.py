"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""


def product_to_str(product):
    """
    Function that formats the product given as argument to a string and returns it.
    This is used to store the products in the dictionaries and to make hashing easier.

    :type product: Product
    :param product: the product to be formated to a string
    """
    # The attribute type is used to find out whether the product is Tea or Coffee
    if hasattr(product, 'type'):
        product_string = "Tea {} {} {}".format(product.name, product.price, product.type)
    else:
        product_string = "Coffee {} {} {} {}".format(product.name, product.price,
                                                     product.acidity, product.roast_level)
    return product_string

def check_key(dictionary, key):
    """
    Simple function to find out if the key exists in the dictionary

    :type dictionary: dict
    :param dictionary: dictionary to look into for the key

    :type key: any
    :param key: key to check if exists in the dict
    """
    return key in dictionary.keys()

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.size = queue_size_per_producer
        self.products_dict = {}         # dict {str:int} <=> {product:quantity}
        self.carts_dict = {}            # dict {int:{str:int}} <=> {cart_id:{product:quantity}}
        self.products_raw = {}          # dict {str:Product} used for reversing to product from str
        self.producers_ids = 0          # int used to give each producer an id
        self.carts_ids = 0              # int used to give each cart an id

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        p_id = "id" + str(self.producers_ids)
        self.producers_ids += 1
        return p_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        product_string = product_to_str(product[0])
        new_quantity = product[1]
        if check_key(self.products_dict, product_string) is True:
            new_quantity = self.products_dict[product_string] + product[1]

        self.products_raw.update({product_string:product[0]})
        self.products_dict.update({product_string:new_quantity})
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.carts_ids += 1
        return self.carts_ids

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        product_string = product_to_str(product['product'])

        if check_key(self.products_dict, product_string) is False:
            return False

        prod_left = self.products_dict.get(product_string) - product['quantity']

        if prod_left < 0:
            return False

        prod_in_cart = product['quantity']
        if check_key(self.carts_dict, cart_id) is True:
            if check_key(self.carts_dict[cart_id], product_string) is True:
                prod_in_cart += self.carts_dict[cart_id].get(product_string)

        self.carts_dict.setdefault(cart_id, {}).update({product_string:prod_in_cart})
        self.products_dict.update({product_string:prod_left})

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        product_string = product_to_str(product['product'])
        if check_key(self.carts_dict, cart_id) is False or check_key(self.carts_dict[cart_id],
                                                                     product_string) is False:
            return False
        else:
            prod_left = self.carts_dict[cart_id].get(product_string)
            prod_left -= product['quantity']
            if prod_left < 0:
                return False

            self.carts_dict[cart_id].update({product_string:prod_left})
            prod_to_add = product['quantity'] + self.products_dict[product_string]
            self.products_dict.update({product_string:prod_to_add})

        return True

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        cart_products = []      # the list of Products to be returned
        if check_key(self.carts_dict, cart_id) is True:
            for key in self.carts_dict[cart_id].keys():
                nr_of_products = self.carts_dict[cart_id][key]  # the quantity of each product in
                                                                # the cart
                for i in range(nr_of_products):
                    cart_products.append(self.products_raw[key])    # a Product is appended
            return cart_products
