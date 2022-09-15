from django.shortcuts import render,HttpResponse
from .models import Employee, Department, Role
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request,template_name='emp_app/index.html')

def view_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps':emps,
    }
    return render(request, template_name='emp_app/view_emp.html', context=context)

def add_emp(request):

    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        department = int(request.POST['department'])
        role = int(request.POST['role'])

        new_emp = Employee(firstName=firstName,
                           lastName=lastName,
                           salary=salary,
                           bonus=bonus,
                           phone=phone,
                           department_id=department,
                           role_id=role,
                           hiredate=datetime.now()
                           )
        new_emp.save()
        return HttpResponse("Employee added successfully")
    return render(request, template_name='emp_app/add_emp.html')

def remove_emp(request, empID = 0):
    if empID:
        try:
            emp_to_be_removed = Employee.objects.get(id=empID)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except:
            return HttpResponse("Enter a valid employee id")

    emps = Employee.objects.all()
    context = {
        'emps': emps,
    }
    return render(request, template_name='emp_app/remove_emp.html', context=context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        department = request.POST['department']
        role = request.POST['role']
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(firstName__icontains = name) | Q(lastName__icontains = name))

        if department:
            emps = emps.filter(department__name__icontains = department)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps':emps
        }
        return render(request, template_name='emp_app/view_emp.html', context=context)
    elif request.method == 'GET':
        return render(request, template_name='emp_app/filter_emp.html')
    else:
        return HttpResponse("An Error Occured")