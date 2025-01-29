from django.db import IntegrityError
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from .models import Customer


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        # Create a new Customer instance when the user logs in for the first time
        try:
            customer = Customer.objects.create(
                name=claims.get('name', ''),
                code=claims.get('sub', ''),  # The 'sub' claim typically holds the unique user ID
                email=claims.get('email', ''),
                phone_number=claims.get('phone_number', ''),  # You can fetch phone from the claims if available
            )
            return customer
        except IntegrityError:
            # Handle cases where a duplicate email or code exists
            return None

    def update_user(self, user, claims):
        # Update the Customer model attributes when a customer logs in again
        if user:
            user.name = claims.get('name', user.name)
            user.email = claims.get('email', user.email)
            user.phone_number = claims.get('phone_number', user.phone_number)
            user.save()
        return user

    def authenticate(self, request, **kwargs):
        # You can extend this method to ensure you're using OpenID connect properly for authentication
        user = super().authenticate(request, **kwargs)
        if user:
            # After authentication, update or create user info
            claims = kwargs.get('claims', {})
            customer = self.update_user(user, claims)
            if not customer:
                # Handle case when the customer does not exist or failed to update
                customer = self.create_user(claims)
        return customer