from django.contrib import admin
from .models import Category,Expenses

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display=('amount','date','description','owner', 'category',)
    search_fields=('amount','category','description', 'date',)
    list_per_page =5

admin.site.register(Expenses,ExpenseAdmin)
admin.site.register(Category)
