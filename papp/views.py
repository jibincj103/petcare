from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.db import connection
from .models import User
from django.contrib.auth import authenticate, login
from .models import Appointment
from .models import Service
from .models import Employee_register,PasswordReset
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import cart
from django.shortcuts import get_object_or_404
from .models import DoctorReport
from django.http import HttpResponse
from .forms import DoctorRegisterForm
from .forms import EmployeeRegisterForm
from .forms import AppointmentForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay

# Create your views here.
def about(r):
    return render(r,'about.html')

def blog(r):
    return render(r,'blog.html')

def services(r):
    return render(r,'service.html')

@login_required(login_url="log")
def contact_us(request):
    if request.method == "POST":
        Name = request.POST.get('name')
        YourPhone = request.POST.get('phone')
        YourEmail = request.POST.get('mail')
        Message = request.POST.get('message')

        data=msg.objects.create(name=Name,mobile=YourPhone,email=YourEmail,message=Message)
        data.save()
        messages.success(request, " Saved successfully")
        return render(request,'contact.html')
    return render(request,'contact.html')

def list_messages(request):
    messages = msg.objects.all()
    return render(request, 'contactasview.html', {'messages': messages})

@login_required(login_url="log")
def newsletter(request):
    if request.method == "POST":
        Name = request.POST.get('name')
        YourEmail = request.POST.get('mail')

        data=newsl.objects.create(name=Name,email=YourEmail)
        data.save()
        messages.success(request, " Saved successfully")
        return render(request,'navd.html')
    return render(request,'navd.html')

def index(r):
    return render(r,'index.html',{})

def price(r):
    return render(r,'price.html')

# def appointment(r):
#     return render(r,'drapprovel.html')

def drpage(r):
    return render(r,'drpage.html')




def emppage(r):
    return render(r,'emppage.html')

# def services(r):
#     return render(r,'service.html')


def single(r):
    return render(r,'single.html')

def p1(r): 
    return render(r,'p1.html')



def tes(request):
    return render(request, 'test.html')



def navvvv(r):
    return render(r,'navvvv.html')

# ............................................................................





def master_reg(request):
    if request.method == 'POST':
        use = request.POST['use']
        pas =  request.POST['pas']
        master.objects.create(username=use,password=pas)
        return redirect('/master')
    else:
        return render(request,'master_reg.html')
    




def masterlogin(request):
    if request.method == 'POST':
        no = request.POST.get('no')
        pa = request.POST.get('pwd')
        
        try:
            user = master.objects.get(username=no)
            if user.password == pa:
                request.session['master'] = no
                messages.success(request, 'Login Successful')
                return render(request, 'adminpage.html')
            else:
                messages.error(request, 'Incorrect Password')
        except master.DoesNotExist:
            messages.error(request, 'Invalid Username')
    
    return render(request, 'masterlog.html')

def masterlogout(request):
    if 'master' in request.session:
        auth.logout(request)
        messages.success(request, 'Logout Successful')
    return redirect('masterlogin') 


# .......................................................................



@login_required(login_url="log")
def appointment(request):
    if request.method == "POST":
        type = request.POST.get('type')
        name = request.POST.get('name')
        age = request.POST.get('a')
        date = request.POST.get('setTodaysDate')
        doctor_id = request.POST.get('doctor') 
        
        # Retrieve the logged-in user
        customer = request.user
        
        # Fetch the selected doctor object
        doctor = dr_register.objects.get(emp_id=doctor_id)
        
        if type == 'Dog':
            price = 299 
        elif type == 'Cat':
            price = 259  
        elif type == 'Mouse':
            price = 399 
        else:
            price = 499 
        
        # Create the appointment object with the associated customer and doctor
        obj = Appointment.objects.create(customer=customer, name=name, type=type, age=age, date=date, price=price, approval=False, doctor=doctor)
        obj.save()
        messages.success(request, "Appointment request sent successfully")  
        
        # Pass the appointment object to the confirmation page
        return redirect('appointment_confirmation', appointment_id=obj.id)  # Redirect to confirmation page after booking
    
    doctors = dr_register.objects.all()  # Fetch all doctors
    return render(request, 'appoin.html', {'doctors': doctors})


def drapplist(request):
    print(request.session['dr_register'])
    data=dr_register.objects.get(name=request.session['dr_register'])
    appointments = Appointment.objects.filter(doctor=data).order_by('date')
    print(appointments)
    return render(request, 'drapplist.html', {'appointments': appointments})


def appointment_confirmation(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'appointment_confirmation.html', {'appointment': appointment})


def appointment_requests(request):
    data=dr_register.objects.get(name=request.session['dr_register'])
    appointment_requests = Appointment.objects.filter(approval=False,doctor=data)
    return render(request, 'appointment_list.html', {'appointment_requests': appointment_requests})

def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.approval = True
    appointment.save()
    messages.success(request, "Appointment approved successfully")
    return redirect('appointment_requests')

def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    # Redirect to the appointment requests page after rejection
    return redirect('appointment_requests') 


def payment(request,id):
        p=Appointment.objects.get(pk=id)
        a = p.price 
        amount=a* 100
        order_currency= 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        
        # payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
        return render(request, "payment.html",{'amount':amount,'id':id})



def paymentservice(request,id):
        p=Service.objects.get(pk=id)
        a = p.price 
        amount=a* 100
        order_currency= 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        
        # payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
        return render(request, "paymentser.html",{'amount':amount,'id':id})


def successs(request, appointment_id):
    print("IN SUCCESS")
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.payment='paid' 
    print(appointment.name,appointment.type,appointment.payment)
    appointment.save()
    return render(request, "success.html",{'appointment': appointment})


def successser(request, service_id):
    print("IN SUCCESS")
    service = Service.objects.get(id=service_id)
    service.payment='paid' 
    print(service.name,service.service_type,service.payment)
    service.save()
    return render(request, "succeessser.html",{'Service': service})

# ...........................................................................



@login_required(login_url="log")
def booking(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            pet_name = request.POST.get('petnam')
            age = request.POST.get('a')
            contact_no = request.POST.get('phn')
            date = request.POST.get('setTodaysDate')
            service_type = request.POST.get('serv')

            if service_type == '1':
                price = 399.00  
            elif service_type == '2':
                price = 599.00 
            elif service_type == '3':
                price = 999.00 
            else:
                price = 0.00

           
            obj = Service.objects.create(
                customer=request.user,
                name=name,
                pet_name=pet_name,
                age=age,
                contact_no=contact_no,
                date=date,
                service_type=service_type,
                price=price
            )
            obj.save()
            messages.success(request, "Service confirmed successfully!")
            
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'booking.html')


def mark_service_as_done(request, service_id):
    # Retrieve the service object
    service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        # Check if the service is already marked as done
        if service.done:
            messages.error(request, 'Service is already marked as done.')
        else:
            # Mark the service as done
            service.done = True
            service.save()
            messages.success(request, 'Service marked as done successfully.')

    # Redirect back to the page where the button was clicked
    return redirect('empserlist')  # Assuming you have a URL named 'service_list'


def thanku(r):
    return render(r,'thankyou.html')


def usrreg(request):
    if request.method == "POST":
        name = request.POST.get('n')
        un = request.POST.get('un')
        p1 = request.POST.get('pwd')
        p2 = request.POST.get('pwd1')
        em = request.POST.get('mail')

        if p1 == p2:
            if User.objects.filter(username=un).exists():
                messages.info(request, 'Username already registered. Please choose another one.')
            elif User.objects.filter(email=em).exists():
                messages.info(request, 'Email already registered.')
            else:
                usr = User.objects.create_user(username=un, first_name=name, email=em, password=p1)
                usr.save()
                messages.success(request, 'User registered successfully.')
                return redirect('log')  # Redirect to home page after successful registration
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'defusr.html')



def usrlogin(request):
    if request.method == 'POST':
        username = request.POST.get('no')
        password = request.POST.get('pwd')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful')
            return render(request, 'index.html')
        else:
            messages.error(request, 'Invalid Username or Password')
    
    return render(request, 'log.html')


# def logout(r):
    #   auth.logout(r)
    #   return redirect(index)

def sign_out(request):
    logout(request)
    request.session.delete()
    return redirect(index)



def adminp(request):
        return render(request,'adminpage.html')



def drpag(request):
        return render(request,'drpage.html')


def drpage2(request):
        return render(request,'drpage1.html')
    
    
def emppage1(request):
        return render(request,'emppage1.html')
# .............................................................................



def employeereg(request):
    if request.method == "POST":
        img= request.FILES.get('img')
        nam = request.POST.get('nam')
        qualif = request.POST.get('qualif')
        ad= request.POST.get('ad')
        con = request.POST.get('con')
        emai = request.POST.get('emai')
        pa=request.POST.get('pa')
        id_card = request.FILES.get('id_card')
        
        objj = Employee_register.objects.create(name=nam, identity_card=id_card, password=pa,image=img, address=ad, qualifications=qualif,contact_no=con, email=emai)
        objj.save()
        print(objj)
        
        
    return render(request, 'employeereg.html')

def emplogin(request):
    if request.method == 'POST':
        no = request.POST.get('no')
        pa = request.POST.get('pa')
        
        try:
            user = Employee_register.objects.get(name=no)
            if user.password == pa:
                request.session['Employee_register'] = no
                messages.success(request, 'Login Successful')
                return render(request, 'emppage1.html')
            else:
                messages.error(request, 'Incorrect Password')
        except Employee_register.DoesNotExist:
            messages.error(request, 'Invalid Username')
    
    return render(request, 'emplog.html')




def approve_employees(request):
    # if not request.user.is_staff:  # Assuming only staff can approve
    #     messages.error(request, 'You are not authorized to view this page.')
    #     return redirect('emplogin')

    if request.method == "POST":
        reg_id = request.POST.get('reg_id')
        action = request.POST.get('action')
        
        try:
            registration = Employee_register.objects.get(emp_id=reg_id)
            if action == 'approve':
                registration.approved = True
                registration.save()
                messages.success(request, f'{registration.name} has been approved.')
            elif action == 'reject':
                registration.delete()
                messages.success(request, f'{registration.name} has been rejected and deleted.')
        except Employee_register.DoesNotExist:
            messages.error(request, 'Registration not found.')

    pending_registrations = Employee_register.objects.filter(approved=False)
    return render(request, 'empregappror.html', {'registrations': pending_registrations})

# .....................................................

def drregisters(request):
    if request.method == "POST":
        img= request.FILES.get('img')
        nam = request.POST.get('nam')
        qualif = request.POST.get('qualif')
        ad= request.POST.get('ad')
        con = request.POST.get('con')
        emai = request.POST.get('emai')
        pa=request.POST.get('pa')
        id_card = request.FILES.get('idcard')
        
        objj = dr_register.objects.create(name=nam, password=pa,identity_card=id_card,image=img, address=ad, qualifications=qualif,contact_no=con, email=emai)
        objj.save()
        print(objj)
        
        
    return render(request, 'drreg.html')

def drlogin(request):
    if request.method == 'POST':
        no = request.POST.get('no')
        pa = request.POST.get('pa')
        
        try:
            user = dr_register.objects.get(name=no)
            if not user.approved:
                messages.error(request, 'Your registration is pending approval.')
            elif user.password == pa:
                request.session['dr_register'] = no
                print(request.session['dr_register'])
                messages.success(request, 'Login Successful')
                return render(request, 'drpage1.html')
            else:
                messages.error(request, 'Incorrect Password')
        except dr_register.DoesNotExist:
            messages.error(request, 'Invalid Username')
    
    return render(request, 'drlogin.html')


def approve_registrations(request):
    # if not request.user.is_staff:  # Assuming only staff can approve
    #     messages.error(request, 'You are not authorized to view this page.')
    #     return redirect('drlog')

    if request.method == "POST":
        reg_id = request.POST.get('reg_id')
        action = request.POST.get('action')
        
        try:
            registration = dr_register.objects.get(emp_id=reg_id)
            if action == 'approve':
                registration.approved = True
                registration.save()
                messages.success(request, f'{registration.name} has been approved.')
            elif action == 'reject':
                registration.delete()
                messages.success(request, f'{registration.name} has been rejected and deleted.')
        except dr_register.DoesNotExist:
            messages.error(request, 'Registration not found.')

    pending_registrations = dr_register.objects.filter(approved=False)
    return render(request, 'drregapppr.html', {'registrations': pending_registrations})


@csrf_exempt
def delete_doctor(request, emp_id):
    if request.method == 'DELETE':
        try:
            doctor = dr_register.objects.get(emp_id=emp_id)
            doctor.delete()  # Delete the instance
            return JsonResponse({'success': True})
        except dr_register.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Doctor not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_employee(request, emp_id):
    if request.method == 'DELETE':
        try:
            employee = Employee_register.objects.get(emp_id=emp_id)
            employee.delete()  # Delete the instance
            return JsonResponse({'success': True})
        except Employee_register.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# ....................................
# forgot_password fir customer

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot_password.html')




def reset_password(request, token):
    try:
        password_reset = PasswordReset.objects.get(token=token)
    except PasswordReset.DoesNotExist:
        # Handle the case where the token does not exist
        return render(request, 'reset_password.html', {'error': 'Invalid or expired token'})

    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        
        if new_password and repeat_password and new_password == repeat_password:
            user = password_reset.user
            user.set_password(new_password)
            user.save()
            password_reset.delete()  # Optionally delete the password reset record after successful reset
            return redirect('index.html')
        else:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match', 'token': token})

    return render(request, 'reset_password.html', {'token': token})

def user_message(req):
    if req.method=='POST':
        nm=req.POST['name']
        email=req.POST['email']
        sub=req.POST['subject']
        msg=req.POST['message']
        send_mail(f'{sub} from user {req.user.email}', f'{msg}','settings.EMAIL_HOST_USER', [email], fail_silently=False)

    return render(req,'user_message.html')




# ......................................



def admincart(request):
    appointments = Appointment.objects.all().order_by('date')
    services = Service.objects.all().order_by('date')
    return render(request, 'admincart.html', {'appointments': appointments, 'services': services})

def appointment_reports(request):
    reports = DoctorReport.objects.all()
    return render(request, 'appointment_reports.html', {'reports': reports})


# ......................................................

def drapplist(request):
    print(request.session['dr_register'])
    data=dr_register.objects.get(name=request.session['dr_register'])
    appointments = Appointment.objects.filter(doctor=data).order_by('date')
    print(appointments)
    return render(request, 'drapplist.html', {'appointments': appointments})



@login_required(login_url="log")
def cart(request):
    appointments = Appointment.objects.filter(customer=request.user).order_by('date')
    services = Service.objects.filter(customer=request.user).order_by('date')
    return render(request, 'cart.html', {'appointments': appointments, 'services': services})



def empserlist(request):
    services = Service.objects.all().order_by('date')
    return render(request, 'empserlist.html', {'services': services})



# def drlistadmin(request):
#     drregister = dr_register.objects.all()
#     return render(request, 'drslistforadmin.html', {'appointments': drregister})



def doctor_register_list(request):
    doctors = dr_register.objects.all().order_by('date')
    return render(request, 'drslistforadmin.html', {'doctors': doctors})




def register_list(request):
    doctors = dr_register.objects.all()
    employees = Employee_register.objects.all()
    return render(request, 'emplist4admin.html', {'doctors': doctors, 'employees': employees})
