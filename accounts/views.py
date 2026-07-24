from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from accounts.forms import AddressForm, ProfileForm, SavedPreferenceForm, UserForm
from accounts.models import Address, SavedPreference


class StoreLoginView(LoginView):
    template_name = "accounts/login.html"


class StoreLogoutView(LogoutView):
    pass



@login_required
def profile(request):
    user_form = UserForm(request.POST or None, instance=request.user, prefix="user")
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile, prefix="profile")
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Profile updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"user_form": user_form, "profile_form": profile_form})


@login_required
def addresses(request):
    form = AddressForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        messages.success(request, "Address saved.")
        return redirect("accounts:addresses")
    return render(request, "accounts/addresses.html", {"form": form, "addresses": request.user.addresses.all()})


@login_required
@require_POST
def delete_address(request, pk):
    get_object_or_404(Address, pk=pk, user=request.user).delete()
    return redirect("accounts:addresses")


@login_required
def wishlist(request):
    return render(request, "accounts/wishlist.html", {"items": request.user.wishlist_items.select_related("product")})


@login_required
def settings(request):
    preference, _ = SavedPreference.objects.get_or_create(user=request.user)
    form = SavedPreferenceForm(request.POST or None, instance=preference)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Preferences saved.")
        return redirect("accounts:settings")
    return render(request, "accounts/settings.html", {"form": form})


password_reset = PasswordResetView.as_view(template_name="accounts/password_reset.html", email_template_name="accounts/password_reset_email.html", success_url=reverse_lazy("accounts:password_reset_done"))
password_reset_done = PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html")
password_reset_confirm = PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html", success_url=reverse_lazy("accounts:password_reset_complete"))
password_reset_complete = PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html")
