from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models import Customer


@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user = instance,
            name = instance.username,
            email = instance.email,
        )
