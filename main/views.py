from django.shortcuts import render
from .forms import LoginForm, TransactionForm
from django.http import HttpResponseRedirect, HttpResponse
from .models import Person
# Create your views here.
import random

def gen_sess_id():
    return random.randint(100000, 999999)

def index(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():

            request.session.set_expiry(0)
            sid = gen_sess_id()
            request.session["user_sess_id"] = sid
            p = Person.objects.get(CardNumber=int(form.cleaned_data["CardNumber"]))
            p.sessionid = sid
            p.save()

            return HttpResponseRedirect("/home/")


    else:
        form = LoginForm()

    return  render(request, "index.html", {"form":form})


def home(request):
    sess_id = int(request.session.get("user_sess_id", None))
    if sess_id:

        try:
            user = Person.objects.get(sessionid=sess_id)
        except Person.DoesNotExist:
            return HttpResponseRedirect("/")
        if request.method == "POST":
            form = TransactionForm(request.POST)
            if form.is_valid():

                type = form.cleaned_data["type"]
                amount = form.cleaned_data["amount"]
                if int(type) == 2:
                    if amount > user.Balance:
                        form.add_error(None, "Amount is much more than the balance")
                    else:
                        user.Balance -= amount
                        user.save()

                else:
                    user.Balance += amount
                    user.save()

        else:
            form = TransactionForm()

        return render(request, "home.html", {"form":form, "balance":user.Balance})
    else:
        return HttpResponseRedirect("/")
