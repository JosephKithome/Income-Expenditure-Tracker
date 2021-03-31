from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import UseIncome,Source
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse
from myUserPreferences.models import MyUserPreferences
import datetime
import csv
import xlwt

#To excel
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum

# Create your views here.
@login_required(login_url = '/authentication/login')
def Index(request):
    sources = Source.objects.all()
    income = UseIncome.objects.filter(owner=request.user)

    #pagination
    paginator = Paginator(income,3)
    page_number =request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    try:
        currency = MyUserPreferences.objects.get(user=request.user).currency
    except MyUserPreferences.DoesNotExist:
        currency =None    
    context ={'sources':sources,
              'income':income,
              'page_obj':page_obj,
              'currency': currency}
    return render(request, 'UserIncome/index.html',context)

@login_required(login_url = '/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {"sources":sources, "values":request.POST}
        
    if request.method=='GET':
        return render(request,'UserIncome/add_income.html',context)  

    if request.method =='POST':
        amount=request.POST['amount']  
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'UserIncome/add_income.html',context) 

    if request.method =='POST':
        description=request.POST['description']  
        if not description:
            messages.error(request,"description is required")
            return render(request,'UserIncome/add_income.html',context)

    if request.method =='POST':
        date=request.POST['date']  
        if not date:
            messages.error(request,"Date is required")
            return render(request,'UserIncome/add_income.html',context)
    if request.method =='POST':
        source = request.POST['source']  
        if not description:
            messages.error(request,"Select is required")
            return render(request,'UserIncome/add_income.html',context) 

    UseIncome.objects.create(owner=request.user, amount=amount,description=description,date=date,source=source)
    messages.success(request,'Income saved successfully')
    return redirect('income')  

def income_edit(request, id):
    income = UseIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context ={
        'income':income,
        'values':income,
        'sources': sources}
    if request.method == 'GET':
        return render(request,'UserIncome/income_edit.html',context)
        

    else:
        if request.method =='POST':
            amount=request.POST['amount']  
            if not amount:
                messages.error(request,"Amount is required")
                return render(request,'UserIncome/income_edit.html',context) 

        if request.method =='POST':
            description=request.POST['description']  
            if not description:
                messages.error(request,"description is required")
                return render(request,'UserIncome/income_edit.html',context)

        if request.method =='POST':
            date=request.POST['date']  
            if not date:
                messages.error(request,"Date is required")
                return render(request,'UserIncome/income_edit.html',context)
        if request.method =='POST':
            source = request.POST['source']  
            if not description:
                messages.error(request,"Select is required")
                return render(request,'UserIncome/income_edit.html',context) 

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()

        messages.success(request,'Record updated successfully')
        return redirect('income')  
def delete_income(request,id):
    income = UseIncome.objects.filter(pk = id)    
    income.delete()
    messages.success(request,"Record was removed")
    return redirect("income")    

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income =UseIncome.objects.filter(
            amount__istartswith=search_str,owner=request.user) | UseIncome.objects.filter(
            date__icontains=search_str,owner=request.user) | UseIncome.objects.filter(
            description__icontains=search_str,owner=request.user) | UseIncome.objects.filter(
            source__icontains=search_str,owner=request.user)
        data = income.values()   
        return JsonResponse(list(data),safe=False)

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    income = UseIncome.objects.filter(owner=request.user, date__gte = six_months_ago,date__lte =todays_date)

    final_income ={}

    def get_source(income):
        return income.source
    def  get_income_category_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)

        for item in filtered_by_source:
            amount +=item.amount
        return amount       

    sources_list = list(set(map(get_source,income)))
    for x in income:
        for y in sources_list:
            final_income[y] = get_income_category_amount(y)    
    
    return JsonResponse({'income_source_data': final_income},safe=False)

def income_stats(request):
    return render(request,'UserIncome/income_stats.html')    

def export_csv(request):     
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Income'+str(datetime.datetime.now())+'.csv'
    writer= csv.writer(response)
    writer.writerow(['Amount','Description','Source','Date']) 

    incomes =UseIncome.objects.filter(owner=request.user)  
    for income in incomes:
        writer.writerow([income.amount,income.description,income.source,income.date])

    return response 

def export_excel(request):
    response = HttpResponse(content_type ='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Income'+str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income')

    row_num = 0
    font_style =xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount','Description','Source','Date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows = UseIncome.objects.filter(owner=request.user).values_list('amount','description','source','date')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]), font_style)

    wb.save(response) 
    return response   


def export_pdf(request):
    response = HttpResponse(content_type ='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename = Income'+str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    income = UseIncome.objects.filter(owner=request.user) 
    sum =income.aggregate(Sum('amount'))
    html_string = render_to_string('UserIncome/pdf_output.html',{'income':income,'total':sum['amount__sum']})
    html = HTML(string=html_string)
    result =html.write_pdf()  
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name,'rb')
        response.write(output.read())

    return response            