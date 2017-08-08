# -*- coding: utf-8 -*-

# Librerias Django:
from django.contrib import admin

# Otros modelos:
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Modelos:
from .models import Profile

# Import-Export
from import_export import resources
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin
from import_export.widgets import Widget
from import_export.widgets import ForeignKeyWidget

# Historia
from simple_history.admin import SimpleHistoryAdmin


class ProfileResource(resources.ModelResource):

    user_username = fields.Field(
        column_name='user_username',
        attribute="user",
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = Profile
        exclude = ('id', )
        fields = (
            'user_username',
            'clave',
            'puesto',
        )
        import_id_fields = ['user_username']


@admin.register(Profile)
class AdminProfile(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ProfileResource
    list_display = (
        'user',
        'puesto',
        'clave',
        'fecha_nacimiento',
        'imagen',
        'firma',
        'comentarios',
    )


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('id', )
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        import_id_fields = ['username']


class UserAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = UserResource
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
