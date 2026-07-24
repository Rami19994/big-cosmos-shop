from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _

from subscriptions.forms import PaymentMethodForm, StoreSetupForm
from subscriptions.models import Store, StoreSubscription, SubscriptionPayment, SubscriptionPlan


def pricing(request):
    return render(request, "subscriptions/pricing.html", {"plans": SubscriptionPlan.objects.filter(is_active=True)})


@login_required
def subscribe(request, plan_code):
    plan = get_object_or_404(SubscriptionPlan, code=plan_code, is_active=True)
    store, _ = Store.objects.get_or_create(owner=request.user, defaults={"name": f"{request.user.get_username()} Store"})
    form = StoreSetupForm(request.POST or None, instance=store)
    billing_cycle = request.POST.get("billing_cycle", StoreSubscription.BillingCycle.MONTHLY)
    if billing_cycle not in StoreSubscription.BillingCycle.values:
        billing_cycle = StoreSubscription.BillingCycle.MONTHLY
    if request.method == "POST" and form.is_valid():
        form.save()
        subscription = StoreSubscription.objects.create(
            store=store,
            plan=plan,
            billing_cycle=billing_cycle,
            amount=plan.price_for(billing_cycle),
        )
        return redirect("subscriptions:payment", subscription_id=subscription.pk)
    return render(request, "subscriptions/subscribe.html", {"plan": plan, "form": form, "billing_cycle": billing_cycle})


@login_required
def payment(request, subscription_id):
    subscription = get_object_or_404(StoreSubscription.objects.select_related("store", "plan"), pk=subscription_id)
    if subscription.store.owner != request.user and not request.user.is_superuser:
        messages.error(request, _("You do not have permission to access this payment."))
        return redirect("subscriptions:pricing")
    form = PaymentMethodForm(request.POST or None)
    payment_record = subscription.payments.first()
    if request.method == "POST" and form.is_valid():
        payment_record = SubscriptionPayment.objects.create(
            subscription=subscription,
            method=form.cleaned_data["method"],
            amount=subscription.amount,
            notes=_("Awaiting payment-provider confirmation or bank-transfer review."),
        )
        messages.success(request, _("Your payment request was recorded. Your plan will activate after payment confirmation."))
        return redirect("subscriptions:payment", subscription_id=subscription.pk)
    return render(request, "subscriptions/payment.html", {"subscription": subscription, "form": form, "payment": payment_record})


@login_required
def my_store(request):
    store = Store.objects.filter(owner=request.user).first()
    if not store:
        return redirect("subscriptions:pricing")
    return render(request, "subscriptions/my_store.html", {"store": store, "subscription": store.active_subscription, "latest_subscription": store.subscriptions.first()})
