from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import SignupForm
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, '회원가입 되었습니다.')

            next_url = request.GET.get('next', 'blog:index') # url reverse 기능
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'form.html', {
        'form': form,
    })

@login_required
def profile_detail(request):
    profile, is_created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'accounts/profile_detail.html', {
    })
