from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.Index, name = "expenses"),
    path('add_expense', views.add_expense,name ='add_expense'),
    path('edit_expense/<int:id>', views.expense_edit,name ='edit_expense'),
    path('delete_expense/<int:id>',views.delete_expense, name ='delete_expense'),
    path('search_text',csrf_exempt(views.search_text), name = 'search_text'),
    path('expense_category_summary',views.expense_category_summary, name = 'expense_category_summary'),
    path('expense_stats', views.expense_stats, name = 'expense_stats'),
    path('export_csv',views.export_csv, name = 'export_csv'),
    path('export_excel',views.export_excel, name ='export_excel'),
    path('export_pdf',views.export_pdf,name ='export_pdf')
]