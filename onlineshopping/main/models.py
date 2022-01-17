from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField('Название', max_length=50)
    model = models.CharField('Модель', max_length=50)
    price = models.IntegerField('Цена')
    stock = models.BooleanField('В наличии')
    picture = models.ImageField('Фотография')

    def __str__(self):
        return self.title

    # @property
    # def imageURL(self):
    #     try:
    #         url = self.picture.url
    #     except:
    #         url = ''
    #     return url


class Category(models.Model):
    title = models.CharField('Модель', max_length=50)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=50, null=True)
    surname = models.CharField('Фамилия', max_length=50, null=True)
    email = models.EmailField('Электронный адрес', null=True)
    phone = models.CharField('Номер телефона', max_length=50, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField('Дата', auto_now_add=True)
    transaction_id = models.CharField('ID Транзакции', max_length=200)
    complete = models.BooleanField('Оплачено', default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        orderitems = self.orderitem_set.all()

        x = []

        for i in orderitems:
            if i.product.stock is True:
                x.append(True)
            else:
                x.append(False)

        if False in x:
            shipping = False
        else:
            shipping = True

        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField('Количество', default=0, null=True, blank=True)
    date_added = models.DateTimeField('Дата', auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingInformation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    city = models.CharField('Область', max_length=200, null=False)
    state = models.CharField('Населенный пункт', max_length=200, null=False)
    address = models.CharField('Адрес', max_length=200, null=False)
    zip_code = models.CharField('Почтовый индекс', max_length=200, null=False)
    date_added = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return self.city


class Receipt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    total_price = models.IntegerField('Сумма', null=False)
    datetime = models.DateTimeField('Дата', auto_now_add=True)
