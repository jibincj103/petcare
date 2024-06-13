"""
URL configuration for ppro project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from papp import views
from django.conf import settings
from django.conf.urls.static import static
from papp.views import tes




urlpatterns = [
    path('admin/', admin.site.urls),
    path('about',views.about,name='about.html'),
    path('blog',views.blog,name='blog.html'),
    path('booking',views.booking,name='booking.html'),
    path('contact',views.contact_us,name='contact.html'),
    path('',views.index,name='index.html'),
    path('price',views.price,name='price.html'),
    path('service',views.services,name='service.html'),
    path('single',views.single,name='single.html'),
    path('p1',views.p1,name='p1.html'),
    path('appointment',views.appointment, name='appointments'),
    path('log',views.usrlogin,name='log'),
    path('logout',views.sign_out,name='logout'),
    path('reg',views.usrreg,name='reg'),
    path('adminadd',views.adminp,name='adminadd'),
    path('drpage',views.drpag,name='drpage'),
    path('drpage1',views.drpage2,name='drpage1'),
    path('employeereg',views.employeereg,name='employeereg'),
    path('emplog',views.emplogin,name='emplog'),
    path('drreg',views.drregisters,name='drregistration'),
    path('drlog',views.drlogin,name='drlog'),
    path('dr.html',views.drpage,name='dr'),
    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='resetpassword'),
    path('test',views.tes,name='test'),
    path('thanku',views.thanku,name='thanku'),
    path('newsletter',views.newsletter,name='newsletter'),
    path('appointments/requests/', views.appointment_requests, name='appointment_requests'),
    path('appointments/approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('appointments/reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('appointment-confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
    path('appointment-reports/', views.appointment_reports, name='appointment_reports'),
    path('admincart', views.admincart, name='admincart'),
    path('cart', views.cart, name='cart'),
    path('empserlist', views.empserlist, name='empserlist'),
    path('drapplist', views.drapplist, name='drapplist'),
    path('emppage',views.emppage,name='emppage'),
    path('emppage1',views.emppage1,name='emppage1'),
    path('navvvv',views.navvvv,name='navvvv'),
    path('approveempreg/', views.approve_employees, name='approveempreg'),
    path('approvedrreg/',  views.approve_registrations, name='approvedrreg'),
    path('doctors/', views.doctor_register_list, name='doctorslist'),
    path('empregisterlist/', views.register_list, name='empregisterlist'),
    path('delete-doctor/<int:emp_id>/', views.delete_doctor, name='delete_doctor'),
    path('delete-employee/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('payment/<int:id>',views.payment,name='payment'),
    path('success/<int:appointment_id>',views.successs,name='success'),
    path('paymentse/<int:id>',views.paymentservice,name='paymentse'),
    path('successs/<int:service_id>', views.successser, name='successs'),
    path('master',views.master_reg,name='/master'),
    path('masterlogin',views.masterlogin,name='/masterlogin'),
    path('messages', views.list_messages, name='messages'),
    path('service/<int:service_id>/mark_as_done/', views.mark_service_as_done, name='mark_service_as_done'),






]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
