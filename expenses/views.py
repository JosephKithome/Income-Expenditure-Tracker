from django.shortcuts import render

# Create your views here.
def Index(request):
    return render(request, 'expenses/index.html')


def add_expense(request):
    return render(request,'expenses/addExpense.html')    
