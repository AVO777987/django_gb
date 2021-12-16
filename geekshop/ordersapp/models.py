from django.db import models
from django.conf import settings

from mainapp.models import Products


class Order(models.Model):
    STATUS_FORMING = 'FM'
    STATUS_SEND_TO_PROCESSED = 'STP'
    STATUS_PROCESSED = 'PRD'
    STATUS_PAID = 'PD'
    STATUS_DONE = 'DN'
    STATUS_CANCELED = 'CN'

    STATUSES = (
        (STATUS_FORMING, 'Формируется'),
        (STATUS_SEND_TO_PROCESSED, 'Отправлен на обработку'),
        (STATUS_PROCESSED, 'Обработан'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_DONE, 'Готов'),
        (STATUS_CANCELED, 'Отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default=STATUS_FORMING, max_length=3)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.product_cost, _items)))

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.product_cost, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


    # def delete(self, *args, **kwargs):
    #     for item in self.orderitems.all():
    #         item.product.quantity += item.quantity
    #         item.product.save()
    #     self.is_active = False
    #     self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Колличество')

    @property
    def product_cost(self):
        return self.quantity * self.product.price

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)
