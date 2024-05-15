from django.contrib import admin
from adoptions.models import Pet, State
# Register your models here.
class PetAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pet, PetAdmin)

class StateAdmin(admin.ModelAdmin):
    pass

admin.site.register(State, StateAdmin)