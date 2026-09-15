from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User
    
# informations generales
    ordering = ["-date_joined"]

    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
    )

   
   
   # informations de l utilisateur
    fieldsets = (
        (
            "Informations personnelles",
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "phone",
                    "address",
                    "city",
                )
            },
        ),

        (
            "Accès au compte",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),

        (
            "Informations du compte",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "last_login",
        "date_joined",
        "updated_at",
    )
    

    # Ajouter un nouvel utilisateur
    add_fieldsets = (
        (
            "Créer un utilisateur",
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

