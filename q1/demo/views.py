from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.forms import ValidationError
from demo.csv_parse import parse_file

# This would be configured with some init parameter or perhaps let the user pick the file somehow through another option on the page.
# For this we'll just have the file in the same directory as this.
filepath = "csvinfo.csv"


# Bad form but I don't wanna deal with auth stuff tbh.
@csrf_exempt
def index(request):
    return render(request, 'demo/home.html', context={})


@csrf_exempt
def post_index(request):
    res = request.POST
    fileMatch = res.get("filename","")
    filesInfo = parse_file(filepath)
    results = []
    # I don't think a malicious payload is part of the scope of this, but if fileMatch is empty, \
    # everything would return back so lets just not allow it.
    if fileMatch != "":
        for file in filesInfo:
            # Q1 just says all results matching name, not starting with and no mention of case sensitivity \
            # so a string in string check is all that we're doing.
            if fileMatch in file["name"]:
                results.append(file)
    responseData = {"results":results}
    return JsonResponse(responseData, safe=False)
