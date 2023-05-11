from django.contrib import admin
from . models import Projects, Services, Contact

# Register your models here.

admin.site.register(Projects)
admin.site.register(Services)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','c_name')
    list_per_page = 10
    
admin.site.register(Contact,ContactAdmin)