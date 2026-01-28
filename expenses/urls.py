from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name="expenses"),
    path('add_expense',views.add_expense,name='add-expense'),
    path('expense-edit/<int:id>',views.Expense_edit,name= 'expense-edit'),
     path('expense-delete/<int:id>',views.Expense_delete,name= 'expense-delete'),
     path('search-expenses',csrf_exempt(views.search_expense),name= 'search-expenses'),
     path(
    'expense_category_summary/',
    views.expense_category_summary,
    name='expense_category_summary'
),
     path('stats', views.stats_view, name='stats'),
      path('export_csv', views.export_csv, name='export-csv'),
      path('export_excel', views.export_excel, name='export-excel'),
      path('export_pdf', views.export_pdf, name='export-pdf'),
]