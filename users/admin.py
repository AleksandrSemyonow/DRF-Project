from django.contrib import admin
from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "first_name", "last_name")
    list_filter = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")


@admin.register(Payment)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "payment_data", "paid_course", "paid_lesson", "payment_amount", "payment_method")
    list_filter = ("user", "payment_data", "paid_course", "paid_lesson", "payment_amount", "payment_method")
    search_fields = ("user", "payment_data", "paid_course", "paid_lesson", "payment_amount", "payment_method")
