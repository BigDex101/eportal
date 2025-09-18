from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Student, Fee, TermInfo, Result, CumulativeResult

def login_view(request):
    if request.method == "POST":
        reg_number = request.POST.get("reg_number")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(reg_number=reg_number)
            if check_password(password, student.password):
                request.session["student_id"] = student.id
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid Registration Number or Password")
        except Student.DoesNotExist:
            messages.error(request, "Invalid Registration Number or Password")

    return render(request, "core/login.html")


def dashboard_view(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("login")

    student = Student.objects.get(id=student_id)
    class_choices = [c for c in Result.CLASS_CHOICES]
    term_choices = [t for t in Result.TERM_CHOICES]
    fees = Fee.objects.all()   # fetch fees
    term_info = TermInfo.objects.last()

    return render(request, "core/dashboard.html", {
        "student": student,
        "class_choices": class_choices,
        "term_choices": term_choices,
        "fees": fees,
        "term_info": term_info,
    })
    
    
def fees_view(request):
    fees = Fee.objects.all()
    resumption_date = "Monday, 15th September, 2025"  # You can also move this to DB later
    return render(request, "core/fees.html", {
        "fees": fees,
        "resumption_date": resumption_date,
    })
    

def result_view(request, student_class, term):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("login")

    student = get_object_or_404(Student, id=student_id)

    results = Result.objects.filter(student=student, student_class=student_class, term=term)

    cumulative_results = []
    if term == "3rd":
        cumulative_results = CumulativeResult.objects.filter(student=student, student_class=student_class)

    return render(request, "core/result.html", {
        "student": student,
        "results": results,
        "cumulative_results": cumulative_results,
        "student_class": student_class,
        "term": term,
    })