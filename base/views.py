from django.shortcuts import render,redirect,get_object_or_404
from .models import Employee,Skill,Work
from django.utils.timezone import now
from django.contrib import messages
from .forms import workform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request):
    employees=Employee.objects.all()
    context={'employees':employees}
    return render(request,'base/home.html',context)

def avaliable(request):
    employees=Employee.objects.filter(availability=True)
    context={'employees':employees}
    return render(request,'base/avaliable.html',context)

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
            print(deadline_difference)
             # Update selected employee if they have lower workload and closer deadlines
            if num_works < min_workload and deadline_difference <= 3:  # Adjust the deadline difference threshold as needed
                 min_workload = num_works
                 selected_employee = employee
                    
                 if selected_employee:
                        work.employee = selected_employee
                        work.save()  # Save the work instance after assigning an employee
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