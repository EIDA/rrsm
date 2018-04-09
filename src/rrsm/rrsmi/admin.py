from django.contrib import admin
from .models import FdsnNode, Link, Profile

class FdsnNodeAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change node details', {
                'fields': [
                    'code',
                    'description',
                    'url_event',
                ]
            }
        ),
    ]

    list_display = (
        'code',
        'description',
        'url_event',
    )

    list_filter = [
        'code',
        'description',
    ]

    search_fields = [
        'code',
    ]


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change profile details', {
                'fields': [
                    'about',
                    'location',
                    'agency',
                    'department',
                    'telephone',
                    'skype',
                    'birth_date',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'user',
        'about',
        'location',
        'birth_date',
    )


class LinkAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change link details', {
                'fields': [
                    'url',
                    'category',
                    'description',
                ]
            }
        ),
    ]

    list_display = (
        'url',
        'category',
        'description',
    )

admin.site.register(FdsnNode, FdsnNodeAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Profile, ProfileAdmin)