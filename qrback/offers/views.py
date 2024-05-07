from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import qrcode
import json
from .models import Offer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def custom_login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=400)

    return JsonResponse({"message": "Only POST requests are allowed"}, status=405)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"csrfToken": request.META.get("CSRF_COOKIE")})

def generate_qr_code(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    url = request.build_absolute_uri(reverse('redeem_offer', args=[offer_id]))
    qr = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response


@csrf_exempt
@login_required
def redeem_offer(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    if offer.redeemed:
        return JsonResponse({"message": "Already redeemed!"}, status=400)

    if request.method == "POST":
        try:
            # Try to parse JSON data
            data = json.loads(request.body)
            confirm = data.get("confirm")
        except json.JSONDecodeError:
            # Fallback to form data
            confirm = request.POST.get("confirm")

        if confirm == "yes":
            offer.redeemed = True
            offer.save()
            return JsonResponse({"message": "Offer redeemed successfully!"})
        else:
            return JsonResponse({"message": "Offer redemption canceled."})

    return JsonResponse({"message": f"Do you want to redeem offer {offer_id}?"})

