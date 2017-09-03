from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from core.forms import SignUpForm, WikiForm

import reversion
from  reversion.models import Version

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            #user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from core.models import Wiki

class WikiPage(View):
    template_name = "wiki/page.html"
    def get(self, request, pageName):
        page = get_object_or_404(Wiki, name=pageName)
        versions = Version.objects.get_for_object(page)
        form = WikiForm(instance=page)
        return render(request, self.template_name, {'page':page,'form':form,'versions':versions})
    def post(self,request,pageName):
        page = get_object_or_404(Wiki, name=pageName)
        versions = Version.objects.get_for_object(page)
        form = WikiForm(request.POST, instance=page)
        if form.is_valid():
            with reversion.create_revision():
                reversion.set_user(request.user)
                reversion.set_comment(form.cleaned_data['commit_message'])
                wikiPage = form.save()
            return redirect('wiki',page.name)
        return render(request, self.template_name, {'page':page,'form':form,'versions':versions})


