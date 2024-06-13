from django.contrib import admin
from .models import Appointment, Employee_register,dr_register,PasswordReset,Service,cart,AppoiCustomerCart,msg,newsl,DoctorCart,DoctorReport

# Register your models here.
admin.site.register([Appointment,Employee_register,dr_register,PasswordReset,Service,cart,AppoiCustomerCart,msg,newsl,DoctorCart,DoctorReport])
