from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages 

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    context = {
        "expenses": expenses
    }

    return render(request, 'expenses/index.html', context)

def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        
    
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category = request.POST.get('category')
        

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        # save expense (example)
        Expense.objects.create(
            amount=amount,
            description=description,
            category=category,
            date=date,
            owner=request.user
        )

        messages.success(request, 'Expense added successfully')
        return redirect('expenses')

def Expense_edit(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'values': expense,
        'categories':categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html',context)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        
    
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category = request.POST.get('category')
        

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        
        expense.owner=request.user
        expense.description=description
        expense.amount=amount
        expense.category=category
        expense.date=date

        expense.save()

        messages.success(request, 'Expense added successfully')
        return redirect('expenses')
    
def Expense_delete(request, id):
    expense = Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request, 'Expense deleted') 
    return redirect('expenses')   
