from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Student(models.Model):
    reg_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.full_name} ({self.reg_number})"


class TermInfo(models.Model):
    term_name = models.CharField(max_length=100, default="1st Term")
    resumption_date = models.DateField()

    def __str__(self):
        return f"{self.term_name} - {self.resumption_date.strftime('%d %B, %Y')}"


class Fee(models.Model):
    class_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.class_name} - ₦{self.amount:,.2f}"


class Result(models.Model):
    CLASS_CHOICES = [
        ("PRY1", "PRY 1"),
        ("PRY2", "PRY 2"),
        ("PRY3", "PRY 3"),
        ("PRY4", "PRY 4"),
        ("PRY5", "PRY 5"),
        ("PRY6", "PRY 6"),
        ("JSS1", "JSS 1"),
        ("JSS2", "JSS 2"),
        ("JSS3", "JSS 3"),
        ("SS1", "SS 1"),
        ("SS2", "SS 2"),
        ("SS3", "SS 3"),
    ]

    TERM_CHOICES = [
        ("1st", "1st Term"),
        ("2nd", "2nd Term"),
        ("3rd", "3rd Term"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="results",
        null=True,
        blank=True
    )
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    subject = models.CharField(max_length=100)
    test1 = models.IntegerField()
    test2 = models.IntegerField()
    test3 = models.IntegerField()
    exam = models.IntegerField()
    term = models.CharField(max_length=10, choices=TERM_CHOICES)

    def total_score(self):
        return self.test1 + self.test2 + self.test3 + self.exam

    def __str__(self):
        return f"{self.student.full_name if self.student else 'Unknown'} - {self.student_class} - {self.subject} ({self.term})"


class CumulativeResult(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="cumulative_results",
        null=True,
        blank=True
    )
    student_class = models.CharField(max_length=10, choices=Result.CLASS_CHOICES, blank=True, null=True)
    subject = models.CharField(max_length=100)
    first_term = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    second_term = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    third_term = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    average = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=2, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        scores = [s for s in [self.first_term, self.second_term, self.third_term] if s is not None]
        if scores:
            self.average = sum(scores) / len(scores)

            if self.average >= 70:
                self.grade = "A"
                self.remarks = "Excellent"
            elif self.average >= 60:
                self.grade = "B"
                self.remarks = "Very Good"
            elif self.average >= 50:
                self.grade = "C"
                self.remarks = "Good"
            elif self.average >= 45:
                self.grade = "D"
                self.remarks = "Fair"
            else:
                self.grade = "F"
                self.remarks = "Poor"

        super().save(*args, **kwargs)

    def __str__(self):
       return f"{self.student.full_name if self.student else 'Unknown'} - {self.student_class} - {self.subject}"
