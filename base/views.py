from django.shortcuts import render,redirect,get_object_or_404
from .models import Employee,Skill,Work
from django.utils.timezone import now
from django.contrib import messages
from .forms import workform,PresenceForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import models
from django.http import HttpResponse
from dotenv import load_dotenv
import os
load_dotenv()
# Create your views here.
def home(request):
    return render(request,'base/home.html')

def allemployees(request):
    page='allemployees'
    employees=Employee.objects.all()
    context={'employees':employees,'page':page}
    return render(request,'base/avaliable.html',context)

def avaliable(request):
    page='avaliable'
    employees=Employee.objects.filter(availability=True)
    context={'employees':employees,'page':page}
    return render(request,'base/avaliable.html',context)

def myworks(request):
    works = Work.objects.filter(employee__name=request.user.username)
    context={'works':works}
    return render(request,'base/myworks.html',context)


def mark_work_completed(request):
    if request.method == 'POST':
        work_id = request.POST.get('work_id')
        work = Work.objects.get(id=work_id)
        
        # Check if the checkbox for completion was checked
        if 'completed' in request.POST:
            work.completed = True
            work.save()
            
            task_link = request.POST.get('task_link')
            work.task_link = task_link
            
            work.save()
            print(os.environ.get('EMAIL_HOST_USER'))
            # Send email
            send_mail(
                'Work Completed',
                f'The work has been marked as completed. Task link: {task_link}',
                work.employee.email,
                [os.environ.get('EMAIL_HOST_USER')],
                fail_silently=False,
            )
            
            messages.success(request, 'Work marked as completed and email sent successfully.')
            return redirect('home')
        else:
            messages.warning(request, 'Checkbox for completion not checked.')
            return redirect('home')  
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('home')  
    

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST' :
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not Exists")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
             

    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def addwork(request):
    form=workform()
    if request.method == 'POST':
        form = workform(request.POST)
        if form.is_valid():
            deadline = form.cleaned_data.get('deadline')
            if deadline < now().date():
                form.add_error('deadline', "Deadline cannot be in the past.")
            else:
                form.save()
                return redirect('home')
    context = {'form': form}
    return render(request, 'base/form.html', context)
def assign_work_view(request):
    page='assign_work'
    works=Work.objects.filter(employee=None)
    context={'works':works,'page':page}
    return render(request, 'base/works.html', context)

def assign_work(request,work_id):
    work= Work.objects.get(pk=work_id)
    eligible_employees = Employee.objects.filter(skills__in=work.skills_needed.all())
    eligible_employees=eligible_employees.filter(availability=True)
    if eligible_employees.exists():
    # Find the employee with the least workload and suitable deadlines
        selected_employee = None
        min_workload = 3
        for employee in eligible_employees:
            # Count the number of works assigned to the employee
            num_works = employee.work_set.all().count()
            # Calculate the difference between the new work's deadline and the latest deadline of the work assigned to the employee
            latest_deadline = employee.work_set.latest('deadline').deadline if employee.work_set.exists() else work.deadline
            deadline_difference = abs((work.deadline - latest_deadline).days)
             # Update selected employee if they have lower workload and closer deadlines
            if num_works < min_workload and deadline_difference > 3:  # Adjust the deadline difference threshold as needed
                 min_workload = num_works
                 selected_employee = employee
                 if selected_employee:
                        work.employee = selected_employee
                        work.save()  # Save the work instance after assigning an employee
                        page_url = f"http://127.0.0.1:8000/viewwork/{work.id}"
                        try:
                            send_mail(
                            'New Task Assigned',
                            f'{work.name} has been assigned to you. Click here to view the details: {page_url}',
                            os.environ.get('EMAIL_HOST_USER'),
                            [selected_employee.email],
                            fail_silently=False,
                        )
                        except Exception as e:
                            print(f"An error occurred while sending email: {e}")
                        return redirect('home')
            else:
                # Handle case when no suitable employee is found
                return render(request, 'base/no_suitable_employee.html')
    else:
        return render(request, 'base/no_eligible_employee.html')
    return render(request, 'base/home.html',)

def viewwork(request):
    page='view'
    works=Work.objects.all()
    context={'works':works,'page':page}
    return render(request, 'base/works.html', context)

def viewspecificwork(request,pk):
    page='specificwork'
    work=Work.objects.get(pk=pk)
    context={'work':work,'page':page}
    return render(request, 'base/works.html', context)


def modifywork(request,work_id):
    work_instance = get_object_or_404(Work, pk=work_id)

    if request.method == 'POST':
        # Populate the form with the data from the POST request and the retrieved work instance
        form = workform(request.POST, instance=work_instance)
        if form.is_valid():
            # Save the updated work instance
            form.save()
            return redirect('home')
    else:
        # Populate the form with the data from the retrieved work instance
        form = workform(instance=work_instance)

    context = {'form': form}
    return render(request, 'base/form.html', context)

def update_presence(request):
    if request.method == 'POST':
        form = PresenceForm(request.POST)
        if form.is_valid():
            employee = Employee.objects.get(name=request.user.username)
            if form.cleaned_data['is_present'] == True:
                employee.availability =True
            if form.cleaned_data['is_absent']==True:
                employee.availability =False
            employee.save()
            return redirect('home')
    else:
        form = PresenceForm()
    return render(request, 'base/update_presence.html', {'form': form})