from django.contrib import admin

from .models import ConsultaCliente, Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "visible")
    list_display_links = ("nombre",)
    list_editable = ("precio", "stock", "visible")
    list_filter = ("categoria", "visible")
    search_fields = ("nombre", "descripcion")

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff


@admin.register(ConsultaCliente)
class ConsultaClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "producto_interes", "fecha", "respondida_en")
    list_filter = ("fecha", "producto_interes")
    search_fields = ("nombre", "correo", "mensaje")
    readonly_fields = ("fecha", "respondida_en", "respondida_por")
    ordering = ("-fecha",)

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

