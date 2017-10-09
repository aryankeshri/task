from django.contrib import admin


from .models import *


class TaskUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'created')
    search_fields = ('email',)
    list_filter = ('role',)

    class Meta:
        model = TaskUser


admin.site.register(TaskUser, TaskUserAdmin)
