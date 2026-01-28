from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import Userpreferences
from .models import Source, Userincome

# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Userincome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Userincome.objects.filter(
            date__istartswith=search_str, owner=request.user) | Userincome.objects.filter(
            description__icontains=search_str, owner=request.user) | Userincome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    
@login_required(login_url='/authentication/login')
def index(request):
    categories = Source.objects.all()
    income = Userincome.objects.filter(owner = request.user)
    paginator = Paginator(income, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = Userpreferences.objects.get(user=request.user).currency
    context = {
        "income": income,
        'page_obj': page_obj,
        'currency': currency
    }

    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('income_date')
        source = request.POST.get('source')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        
        Userincome.objects.create(
            amount=amount,
            description=description,
            source=source,
            date=date,           
            owner=request.user
        )

        messages.success(request, 'Record added successfully')
        return redirect('income')

def Income_edit(request,id):
    income = Userincome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income':income,
        'values': income,
        'sources':sources
    }
    if request.method == 'GET':
        return render(request, 'income/income-edit.html',context)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/income-edit.html', context)
        
    
        description = request.POST.get('description')
        date = request.POST.get('income_date')
        source = request.POST.get('source')
        

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/income-edit.html', context)
        income.description=description
        income.amount=amount
        income.source=source
        income.date=date

        income.save()

        messages.success(request, 'Record updated successfully')
        return redirect('income')
    
def Income_delete(request, id):
    income = Userincome.objects.get(pk = id)
    income.delete()
    messages.success(request, 'income deleted') 
    return redirect('income')   


