from userpreferences.models import UserPreferences
from django.shortcuts import render, redirect
from userincome.models import Source, Income
from userincome.models import Income, Source
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


def index(request):
    categories = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    # currency = UserPreferences.objects.get(user=request.user).currency
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'income': income,
        # 'currency': currency,
         'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'income/index.html', context=context)


def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'income/add_income.html', context=context)
    
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context=context)
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context=context)
        
        Income.objects.create(owner=request.user, amount=amount, date=date,
                               source=source, description=description)
        messages.success(request, 'Income saved successfully')

        return redirect('income')
        
    # return render(request, 'expenses/add_expenses.html', context=context)

def income_edit(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)

        income.owner = request.user
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Income updated  successfully')

        return redirect('income')
    

def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed')
    return redirect('income')