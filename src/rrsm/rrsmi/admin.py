from django.contrib import admin
from .models import FdsnNode, Link

class FdsnNodeAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change node details', {
                'fields': [
                    'code',
                    'description',
                    'url_event',
                    'url_motion',
                ]
            }
        ),
    ]

    list_display = (
        'code',
        'description',
        'url_event',
        'url_motion',
    )

    list_filter = [
        'code',
        'description',
    ]

    search_fields = [
        'code',
    ]


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
