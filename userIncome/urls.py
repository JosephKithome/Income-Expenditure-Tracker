from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.Index, name = "income"),
    path('add_income', views.add_income,name ='add_income'),
    path('edit_income/<int:id>', views.income_edit,name ='edit_income'),
    path('delete_income/<int:id>',views.delete_income, name ='delete_income'),
    path('search_income',csrf_exempt(views.search_income), name = 'search_income'),
    path('income_stats',views.income_stats, name ='income_stats'),
    path('income_source_summary',views.income_source_summary, name = 'income_source_summary'),
    path('income_export_csv',views.export_csv, name ='income_export_csv'),
     path('income_export_excel',views.export_excel, name ='income_export_excel'),
    path('income_export_pdf',views.export_pdf,name ='income_export_pdf')
]