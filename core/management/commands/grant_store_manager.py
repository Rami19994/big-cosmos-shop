from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Grants a user access to manage only the products they own."

    def add_arguments(self, parser):
        parser.add_argument("username", help="Username of the store manager")

    def handle(self, *args, **options):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=options["username"])
        except user_model.DoesNotExist as error:
            raise CommandError("No user exists with that username.") from error

        if user.is_superuser:
            raise CommandError("A superuser already has full access and cannot be made a limited store manager.")

        group, _ = Group.objects.get_or_create(name="Store managers")
        permissions = Permission.objects.filter(
            content_type__app_label="products",
            content_type__model="product",
            codename__in=["add_product", "change_product", "delete_product", "view_product"],
        )
        group.permissions.set(permissions)
        user.groups.add(group)
        user.is_staff = True
        user.save(update_fields=["is_staff"])
        self.stdout.write(self.style.SUCCESS(f"{user.get_username()} can now manage only their own products."))
