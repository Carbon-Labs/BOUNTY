from django.contrib import admin

from . import models

class TasksInline(admin.TabularInline):
    model = models.Tasks
    fields = ('short_description', 'reference','budget', 'funding', 'remaining')
    readonly_fields = ('funding', 'reference', 'remaining')

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('reference',)
    #fields = (('name', 'reference'),'slug')
    fieldsets = (
        ('Basic Details', {
            'fields' : (('name', 'reference'),'client','slug','thumbnail'),
        }),
        ('Category', {
            'classes': ('collapse',),
            'fields' : ('category', 'subcategory'),
        }),
        ('Description', {
            'classes': ('collapse',),
            'fields' : ('blurb','description'),
        }),

    )

    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','reference','client','updated_at', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    date_hierarchy = 'created_at'
    inlines = [
        TasksInline,
    ]

@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'email')
    ordering = ('name',)

@admin.register(models.Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'github_name', 'email', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('name', 'github_name', 'email')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'github_name',),
                'email',
                ('company', 'url'),
                'location'
            )
        }),
        ('Profile', {
            'classes': ('collapse',),
            'fields': (
                'bio',
            ),
        })
    )

@admin.register(models.Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

@admin.register(models.SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('name',)
    fields = ('category','name')

class FundingsInline(admin.TabularInline):
    model = models.Fundings

    def has_add_permission(self, request):
        return False

@admin.register(models.Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('project', 'short_description', 'reference', 'budget', 'funding', 'remaining')
    list_display_links = ('short_description',)
    list_filter = ('project',)
    search_fields = ('short_description',)
    inlines = [
        FundingsInline,
    ]


@admin.register(models.FundingMethods)
class FundingMethodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'token_id', 'amount_held', 'url')
    ordering = ('name',)
    search_fields = ('name', 'token_id')

@admin.register(models.Fundings)
class FundingsAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'project', 'task', 'sender', 'token', 'amount')
    ordering = ('created_at',)
    list_filter = ('project', 'token')
    search_fields = ('task',)
