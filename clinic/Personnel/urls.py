from django.urls import path
from .views import EmployeeAdminView

urlpatterns = [
    path('employee_admin/', EmployeeAdminView.as_view(), name = 'employee_admin'),
]