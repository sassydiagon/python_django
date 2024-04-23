from django.contrib import admin
from django.db.models import Sum
from .models import Student, Subject, Marks

class MarksInline(admin.TabularInline):
    model = Marks
    extra = 0
    fields = ('subject', 'marks_obtained')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs["queryset"] = Subject.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj and obj.class_in:
            subjects = Subject.objects.filter(class_in=obj.class_in)
            formset.form.base_fields['subject'].queryset = subjects
        return formset

class StudentAdmin(admin.ModelAdmin):
    inlines = [MarksInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'roll_number', 'dob', 'class_in')
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_marks=Sum('marks__marks_obtained'))
        return queryset

    def total_marks(self, obj):
        return obj.total_marks

    total_marks.admin_order_field = 'total_marks'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "class_in":
            kwargs["queryset"] = Subject.objects.values_list('class_in', flat=True).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
