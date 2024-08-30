
from django.shortcuts import render, redirect
from . import forms
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import login
from django.views.generic import View


# todo api view où on ne définit que le post, vérification des mots de passe (identiques ? ) si oui, créer user
class SignupPage(View):
    form = forms.SignupForm

    def get(self, request):
        form = forms.SignupForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if request.method == "POST":
            form = forms.SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name, context={"form": form})


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
