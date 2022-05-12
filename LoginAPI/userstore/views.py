from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from LoginAPI import settings
from datetime import timedelta
import json

@csrf_exempt
def user(request, token=None):
    if request.method == "POST":
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        try:
            User.objects.get(username=email)
            return HttpResponse(json.dumps({"message": "User exists in database."}, indent=2,separators=(',', ': ')),
                                content_type="application/json", status=403)
        except:
            user = User.objects.create_user(username=email)
            user.email = email
            user.set_password(passwd)
            user.is_active = False
            user.save()
            return HttpResponse(json.dumps({"message": "User successfully created!"}, indent=2,separators=(',', ': ')),
                                content_type="application/json", status=200)

    if request.method == "DELETE":
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        try:
            user = User.objects.get(username=email, password=passwd)
            user.delete()
        except:
            return HttpResponse(json.dumps({"message": "User doesn't exist in database."}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=404)

        return HttpResponse(json.dumps({"message": "User successfully deleted!"}, indent=2, separators=(',', ': ')),
                            content_type="application/json", status=200)

    if request.method == "GET":
        if token:
            try:
                user = User.objects.get(id=token)
                user.is_active = True
                user.save()
                return HttpResponse(json.dumps({"message": "User successfully activated!"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=200)
            except:
                return HttpResponse(json.dumps({"message": "User already active!"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=400)
        else:
            return HttpResponse(json.dumps({"message": "Ivalid token"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=404)

@csrf_exempt
def user_passwd(request):
    if request.method == "PATCH":

        email = request.POST.get('email')
        old_passwd = request.POST.get('old_passwd')
        new_passwd = request.POST.get('new_passwd')
        try:
            User.objects.get(username=email, password=old_passwd)
            return HttpResponse(json.dumps({"message": "Ivalid email or password"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=404)
        except:
            user = User.objects.create_user(username=email)
            user.email = email
            user.set_password(new_passwd)
            user.save()
            return HttpResponse(json.dumps({"message": "Password sucessfully changed"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=200)

@csrf_exempt
def token(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        try:
            User.objects.get(username=email, password=passwd)
            token = request.session._get_or_create_session_key()
            token.set_expiry(timedelta(seconds=settings.SESSION_COOKIE_AGE))
            return HttpResponse(json.dumps({"token": f"{token}"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=200)
        except:
            return HttpResponse(json.dumps({"message": "Ivalid email or password"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=404)

@csrf_exempt
def token_refresh(request):
    if request.method == "PATCH":

        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        try:
            User.objects.get(username=email, password=passwd)
            token = request.session._get_or_create_session_key()
            token.set_expiry(timedelta(seconds=settings.SESSION_COOKIE_AGE))
            return HttpResponse(json.dumps({"JWT_TOKEN": f"{token}"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=200)
        except:
            return HttpResponse(json.dumps({"JWT_TOKEN": f"{token}"}, indent=2, separators=(',', ': ')),
                                content_type="application/json", status=200)
