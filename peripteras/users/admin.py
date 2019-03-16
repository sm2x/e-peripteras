from django.contrib import admin

from peripteras.users.models import SimpleUser, Addresses, Order, Feedback

@admin.register(SimpleUser)
class SimpleUserAdmin(admin.ModelAdmin):
    model = SimpleUser
    list_display = ('user','id' ) 

@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    model = Addresses

    list_display = ('id', 'user')
    def user(self, obj):
        return SimpleUser.objects.get(id=obj.simple_user_id)

    user.short_description = 'Address owns to:' 
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('kiosk','id', 'total_sum', 'address' ) 

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ('stars','order','simple_user' ) 
