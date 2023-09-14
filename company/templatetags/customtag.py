from django import template
from ..models import Notifications  

register = template.Library()

@register.simple_tag
def get_notifications(ruser):
    
    data = Notifications.objects.filter(user = ruser)  
    return data