from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Student, Fee, TermInfo, Result, CumulativeResult


# ✅ Admin site customization (default admin, no override)
admin.site.site_header = "St. Lawrence School Portal"
admin.site.site_title = "School Portal Admin"
admin.site.index_title = "Manage Students, Results, and Fees"

# ✅ Inject custom CSS for all admin pages
class AdminMedia:
    class Media:
        css = {
            "all": ("core/css/admin.css",)  # your custom admin CSS
        }

# Attach custom Media to all ModelAdmin classes
admin.ModelAdmin.__bases__ += (AdminMedia,)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('reg_number', 'full_name')
    search_fields = ('reg_number', 'full_name')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:  # Hash only if password was modified
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ("class_name", "amount")


@admin.register(TermInfo)
class TermInfoAdmin(admin.ModelAdmin):
    list_display = ("term_name", "resumption_date")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "student_class", "subject", "term")
    list_filter = ("student_class", "term", "student")

    @admin.display(description="Total Score")
    def total_score(self, obj):
        return obj.total_score()


@admin.register(CumulativeResult)
class CumulativeResultAdmin(admin.ModelAdmin):
    list_display = ("student", "student_class", "subject", "average", "grade", "remarks")
    list_filter = ("student", "student_class", "grade")