from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Basket

CustomUser = get_user_model()

@receiver(user_logged_in, sender=CustomUser)
def merge_cart(sender, request, user, **kwargs):
    old_session_key = request.session.pop("old_session_key", None)  # Retrieve and remove old session key
    
    if old_session_key:
        cart_items = Basket.objects.filter(session_key=old_session_key)  # Filter by old session key

        for item in cart_items:
            existing_item = Basket.objects.filter(session_key=request.session.session_key, product=item.product).first()

            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
                item.delete()
            else:
                item.session_key = request.session.session_key
                item.save()