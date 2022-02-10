from django.shortcuts import render
from customer.models import Customer
# Create your views here.
def index(request):
    print("naw")
    # return (request, "printing")

def customer_view(request):
    customer = Customer.objects.all()
    context={'customers': customer}
    return render(request, "file.html", context)
