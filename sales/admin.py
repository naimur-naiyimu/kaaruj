from django.contrib import admin
from .models import *
# Register your models here.


class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('number', "created_by")
    list_display = ('number', 'slug','id')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


admin.site.register(Invoice, InvoiceAdmin)
