from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="expenses"),
    path('add_expense',views.add_expense,name='add-expense'),
    path('expense-edit/<int:id>',views.Expense_edit,name= 'expense-edit'),
     path('expense-delete/<int:id>',views.Expense_delete,name= 'expense-delete')
]