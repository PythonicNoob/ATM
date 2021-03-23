from django import forms
from .models import Person

from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    CardNumber = forms.IntegerField(min_value=1000000000000000, max_value=9999999999999999)
    CVV = forms.IntegerField(min_value=100, max_value=999)
    PIN = forms.IntegerField(min_value=1000, max_value=9999)
    # class Meta:
    #     model = Person
    #     exclude = ['Balance']


    def clean(self):

        cleaned_data = super().clean()
        CardNumber = cleaned_data.get('CardNumber')
        CVV = cleaned_data.get('CVV')
        PIN = cleaned_data.get('PIN')
        print("card number", CardNumber)
        try:
            p = Person.objects.get(pk=CardNumber)

        except Person.DoesNotExist:
            print("Rasing error")
            raise ValidationError("Person with the card number does not exist")
        except Exception as e:
            print(e)

        if p.CVV != CVV: raise ValidationError("Incorrect CVV")
        if p.PIN != PIN: raise ValidationError("Incorrect PIN")



class TransactionForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
    type = forms.ChoiceField(choices=[(1,"Deposit"),(2,"Withdraw")])



