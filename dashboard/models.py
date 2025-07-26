from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class RentPayment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.tenant} - {self.amount}"
