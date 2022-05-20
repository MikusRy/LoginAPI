from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from LoginAPI import settings
from django.utils import timezone
from datetime import timedelta
import json


@csrf_exempt
def user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        try:
            User.objects.get(username=email)
            return HttpResponse(json.dumps({"message": "User exists in database."}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=403)
        except:
            user = User.objects.create_user(username=email)
            user.email = email
            user.set_password(passwd)
            user.is_active = False
            user.save()
            return HttpResponse(json.dumps({"message": "User successfully created!"}, indent=2,separators=(',', ': ')),
                                content_type="application/json", status=200)
    return HttpResponse(json.dumps({"message": "Method not allowed"}, indent=2, separators=(',', ': ')),
                        content_type="application/json", status=405)


@csrf_exempt
def user_delete(request):
    if request.method == "POST":
        token = request.POST.get('token')
        if token:
            try:
                session = Session.objects.get(session_key=token)
                uid = session.get_decoded().get('_auth_user_id')
                user = User.objects.get(id=uid)
                user.delete()
                return HttpResponse(json.dumps({"message": "User successfully deleted!"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=200)
            except:
                return HttpResponse(json.dumps({"message": "User doesn't exist!"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=400)

    return HttpResponse(json.dumps({"message": "Method not allowed"}, indent=2, separators=(',', ': ')),
                        content_type="application/json", status=405)


@csrf_exempt
def user_activate(request):
    if request.method == "POST":
        token = request.POST.get('token')

        user = User.objects.get(id=token)
        user.is_active = True
        user.save()
        return HttpResponse(json.dumps({"message": "User successfully activated!"}, indent=2, separators=(',', ': ')),
                        content_type="application/json", status=200)

    return HttpResponse(json.dumps({"message": "Method not allowed"}, indent=2, separators=(',', ': ')),
                        content_type="application/json", status=405)


@csrf_exempt
def user_passwd(request):
    if request.method == "POST":
        token = request.POST.get('token')
        passwd = request.POST.get('passwd')
        try:
            session = Session.objects.get(session_key=token)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(id=uid)
            user.set_password(passwd)
            user.save()
            return HttpResponse(json.dumps({"message": "Password changed successfully!"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=200)
        except:
            print("")
    return HttpResponse(json.dumps({"message": "Method not allowed"}, indent=2, separators=(',', ': ')),
                        content_type="application/json", status=405)

@csrf_exempt
def token(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        user = authenticate(username=email, password=passwd)
        if user:
            login(request, user)
            logout(request)
            login(request, user)
            token = request.session.session_key
            return HttpResponse(json.dumps({"JWT_TOKEN": f"{token}"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=200)
        return HttpResponse(json.dumps({"message": f"User not found"}, indent=2, separators=(',', ': ')),
                                        content_type="application/json", status=404)
    return HttpResponse(json.dumps({"message": "Method not allowed"}, indent=2, separators=(',', ': ')),
                        content_type="application/json", status=405)

@csrf_exempt
def token_refresh(request):
    if request.method == "POST":
        token = request.POST.get('token')

        session = Session.objects.get(session_key=token)
        if session:
            session.expire_date = timezone.now() + timedelta(seconds=settings.SESSION_COOKIE_AGE)
            session.save()
        return HttpResponse(json.dumps({"JWT_TOKEN": f"{token}"}, indent=2, separators=(',', ': ')),
                            content_type="application/json", status=200)
    return HttpResponse(json.dumps({"message": "Method not allowed"}, indent=2, separators=(',', ': ')),
                        content_type="application/json", status=405)