from django.db import models
from django.contrib.auth.models import User




    
class Employee_register(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='profile_images/')
    address = models.CharField(max_length=150)
    qualifications = models.CharField(max_length=50, blank=True, null=True)
    contact_no = models.BigIntegerField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=15)
    identity_card = models.ImageField(upload_to='identity_cards/')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.emp_id})'
       
    


class dr_register(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='profile_images/')
    address = models.CharField(max_length=150)
    qualifications = models.CharField(max_length=50)
    contact_no = models.BigIntegerField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=15)
    identity_card = models.ImageField(upload_to='identity_cards/')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.emp_id})'
    
class Appointment(models.Model):
    TYPE_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Mouse', 'Mouse'),
        ('Other', 'Other'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    name = models.CharField(max_length=15)
    age = models.IntegerField()
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    approval = models.BooleanField(default=False)
    doctor = models.ForeignKey(dr_register, on_delete=models.CASCADE)
    payment = models.CharField(max_length=20,default='pending',null=True)
    def __str__(self):
        return self.name

class PasswordReset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('1', 'Basic'),
        ('2', 'Standard'),
        ('3', 'Premium'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    pet_name = models.CharField(max_length=30)
    age = models.IntegerField()
    contact_no = models.BigIntegerField()
    date = models.DateTimeField()
    service_type = models.CharField(max_length=1, choices=SERVICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(max_length=20,default='pending',null=True)
    done = models.BooleanField(default=None,null=True)

    def __str__(self):
        return self.name

class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def total_price(self):
        return self.service.price * self.quantity
    
class AppoiCustomerCart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Customer Cart: {self.customer.username}"


class DoctorCart(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Doctor Cart: {self.appointment.name}"


class DoctorReport(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    report = models.TextField()
    rest_time = models.IntegerField(default=0)  # Assuming rest time is in hours
    medicine1 = models.CharField(max_length=50, blank=True, null=True)
    medicine2 = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.appointment.name}"



class msg(models.Model):
    name=models.CharField(max_length=100)
    mobile=models.IntegerField()
    email=models.EmailField()
    message=models.TextField()

    def __str__(self) -> str:
        return f'{self.name}'
    
class newsl(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    

    def __str__(self) -> str:
        return f'{self.name}'
    


class cart(models.Model):
    cartitm=models.ForeignKey(Appointment,on_delete=models.CASCADE)
    count=models.IntegerField(default=0)


class master(models.Model):
  
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=15)
    def __str__(self):
        return self.username
