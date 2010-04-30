from django.db import models
from django.contrib.auth.models import User as AuthUser

class Client(models.Model):
    auth_key = models.CharField(max_length=200)
    name = models.CharField(max_length=200, primary_key=True)

class MachineUser(models.Model):
    user = models.ForeignKey(AuthUser, primary_key=True)
    twitter = models.CharField(max_length=25, blank=True)
    student_id = models.CharField(max_length=10, blank=True)
    balance = models.IntegerField(help_text='measured in pennies', default=0)

class Soda(models.Model):
    short_name = models.CharField(max_length=10, unique=True, primary_key=True)
    description = models.CharField(max_length=200)
    cost = models.IntegerField(help_text='measured in pennies (ie, 500 = $5)')
    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

# The generic transaction model.  Subclass this to model any action that exchanges
# currency between a user's account
class Transaction(models.Model):
    amount = models.IntegerField(help_text='measured in pennies (ie, 500 = $5)')
    user = models.ForeignKey(MachineUser)
    date_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    
    class Meta:
        abstract = True
        ordering = ['-date_time']

# A subclass of Transaction, used to model administrative deposits and withdrawls
# from a user's account (adding money to account or cashing out)
class AdminTransaction(Transaction):
    admin_user = models.ForeignKey(AuthUser)


# A subclass of Transaction, used to model a user purchasing a soda
class SodaTransaction(Transaction):
    soda = models.ForeignKey(Soda)

class Inventory(models.Model):
    soda = models.ForeignKey(Soda, primary_key=True)
    slot = models.PositiveSmallIntegerField()
    amount = models.PositiveSmallIntegerField()

    @staticmethod
    def returnQs(qs):
        output = []
        for i in qs:
            output.append(
            {
                'soda': {
                    'short_name': i.soda.short_name,
                    'description': i.soda.description,
                    'cost': i.soda.cost
                },
                'quantity': i.amount
            })
        return output

    @staticmethod
    def getEntireInventory():
        return Inventory.returnQs(Inventory.objects.select_related(depth=1).all())

    @staticmethod
    def getInventoryForSoda(soda):
        return Inventory.returnQs(Inventory.objects.select_related(depth=1).filter(pk=soda).all())

    @staticmethod
    def getInventoryForSlot(slot):
        return Inventory.returnQs(Inventory.objects.select_related(depth=1).filter(slot=slot).all())

adminable = (Inventory, MachineUser, Soda, Transaction, SodaTransaction, Client)
