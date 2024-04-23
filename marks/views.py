from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from .models import Student, Subject, Marks

def student_form(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        dob = request.POST.get('dob')
        class_in = request.POST.get('class_in')
        
        # Get marks for each subject from the form
        marks = {}
        for subject in Subject.objects.all():
            marks[subject.name] = request.POST.get(subject.name)

        # Perform validation, processing, and saving of the form data
        # (Your implementation goes here)

        # Redirect to a success page
        return redirect('success_page')  # Use URL name for redirection

    else:
        class_in = request.GET.get('class_in')  # Assuming you're passing class_in via AJAX
        if class_in == 'High School':
            subjects = Subject.objects.filter(name__in=['Math', 'Science', 'Social Studies', 'English', 'Hindi'])
        elif class_in == 'Intermediate':
            subjects = Subject.objects.filter(name__in=['Physics', 'Chemistry', 'Math', 'English', 'Hindi'])
        else:
            subjects = None  # Handle this case as needed

        context = {
            'subjects': subjects
        }
        return render(request, 'marks/student_form.html', context)

def submit_student_form(request):
    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        dob = request.POST.get('dob')
        class_in = request.POST.get('class_in')
        # Retrieve subject marks from POST data as needed

        # Create a new Student object and save it to the database
        student = Student.objects.create(
            name=name,
            roll_number=roll_number,
            dob=dob,
            class_in=class_in,
        )

        # Retrieve the subject names based on the selected class
        if class_in == 'High School':
            subjects = ['Math', 'Science', 'Social Studies', 'English', 'Hindi']
        elif class_in == 'Intermediate':
            subjects = ['Physics', 'Chemistry', 'Math', 'English', 'Hindi']

        # Create Marks objects for each subject and save them to the database
        for subject_name in subjects:
            subject, _ = Subject.objects.get_or_create(name=subject_name)
            marks_obtained = request.POST.get(subject_name, 0)  # Default marks as 0 if not provided
            Marks.objects.create(student=student, subject=subject, marks_obtained=marks_obtained)

        # Redirect the user to the success page
        return HttpResponseRedirect('success_page')  # Use URL name for redirection

    else:
        return HttpResponse('Method Not Allowed')

def success_page(request):
    return render(request, 'marks/success_page.html')  # Correct template name

def student_rank(request):
    students = Student.objects.annotate(total_marks=Sum('marks__marks_obtained')).order_by('-total_marks')
    return render(request, 'marks/student_rank.html', {'students': students})
