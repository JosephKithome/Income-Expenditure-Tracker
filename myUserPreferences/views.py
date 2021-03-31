from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import MyUserPreferences
from django.contrib import messages



# Create your views here.
def preferences(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR,'currency.json')
    with open(file_path,'r') as json_file:
        json_data = json.load(json_file)
        for key,value in json_data.items():
            if isinstance(value,dict):
                currency_data.append(value)
        else:        
            currency_data.append({'name':key,'value':value})
           
    exists =MyUserPreferences.objects.filter(user=request.user).exists()
    user_preference =None
    
    if exists:
        user_preference = MyUserPreferences.objects.get(user=request.user)
    

    if request.method =="GET":
        return render(request,'preferences/preferences.html',{'currency_data':currency_data, "user_preference":user_preference})
    else:
        currency = request.POST['currency']
        if exists:
            user_preference.currency =currency
            user_preference.save()
        else: 
            MyUserPreferences.objects.create(user=request.user, currency=currency)   
        messages.success(request,'Changes saved successfully')
        return render(request,'preferences/preferences.html',{'currency_data':currency_data, "user_preference":user_preference})

    