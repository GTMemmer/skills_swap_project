from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SkillForm, UserRegistrationForm, ReviewForm
from .models import Skill, Review


def skill_list(request):
    """Show all posted skills in the marketplace with optional search and filters."""
    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '')
    selected_availability = request.GET.get('availability', '')

    skills = Skill.objects.select_related('owner').all()

    if search_query:
        skills = skills.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(owner__username__icontains=search_query)
        )

    if selected_category:
        skills = skills.filter(category=selected_category)

    if selected_availability:
        skills = skills.filter(availability_status=selected_availability)

    # Paginate results (15 per page)
    paginator = Paginator(skills, 15)
    page_number = request.GET.get('page')
    skills_page = paginator.get_page(page_number)

    # Get stats in a single query
    all_skills = Skill.objects.all()
    stats = all_skills.aggregate(
        total_skills=Count('id'),
        available_count=Count('id', filter=Q(availability_status='available')),
        free_count=Count('id', filter=Q(free=True))
    )

    context = {
        'skills': skills_page,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_availability': selected_availability,
        'categories': Skill.CATEGORY_CHOICES,
        'availability_options': Skill.AVAILABILITY_CHOICES,
        **stats,
    }
    return render(request, 'mainapp/skill_list.html', context)


def skill_detail(request, pk):
    """Show one skill post with full details and reviews."""
    skill = get_object_or_404(Skill, pk=pk)
    reviews = skill.reviews.select_related('user').all()
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to post a review.')
            return redirect('MainApp:login')
        
        if skill.owner == request.user:
            messages.error(request, 'You cannot review your own skill.')
            return redirect('MainApp:skill_detail', pk=pk)

        if user_has_reviewed:
            messages.error(request, 'You have already reviewed this skill.')
            return redirect('MainApp:skill_detail', pk=pk)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.skill = skill
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('MainApp:skill_detail', pk=pk)
    else:
        form = ReviewForm()

    context = {
        'skill': skill,
        'reviews': reviews,
        'form': form,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'mainapp/skill_detail.html', context)


@login_required
def skill_create(request):
    """Allow logged-in users to create a new skill post."""
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user
            skill.save()
            messages.success(request, 'Your skill post has been created.')
            return redirect('MainApp:skill_detail', pk=skill.pk)
    else:
        form = SkillForm()

    return render(request, 'mainapp/skill_form.html', {'form': form, 'form_title': 'Create Skill'})


@login_required
def skill_update(request, pk):
    """Allow the owner to edit their skill posting."""
    skill = get_object_or_404(Skill, pk=pk)
    if skill.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your skill post has been updated.')
            return redirect('MainApp:skill_detail', pk=skill.pk)
    else:
        form = SkillForm(instance=skill)

    return render(request, 'mainapp/skill_form.html', {'form': form, 'form_title': 'Edit Skill'})


@login_required
def skill_delete(request, pk):
    """Allow the owner to delete a skill posting."""
    skill = get_object_or_404(Skill, pk=pk)
    if skill.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill post deleted successfully.')
        return redirect('MainApp:dashboard')

    return render(request, 'mainapp/skill_confirm_delete.html', {'skill': skill})


@login_required
def dashboard(request):
    """Show the logged-in user's own skill posts."""
    skills = Skill.objects.filter(owner=request.user)
    stats = skills.aggregate(
        available_count=Count('id', filter=Q(availability_status='available')),
        free_count=Count('id', filter=Q(free=True))
    )
    context = {
        'skills': skills,
        **stats,
    }
    return render(request, 'mainapp/dashboard.html', context)


def register_user(request):
    """Handle new user registration."""
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect(next_url or 'MainApp:dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'mainapp/register.html', {'form': form, 'next_url': next_url})


def login_view(request):
    """Log a user into the application."""
    next_url = request.GET.get('next', request.POST.get('next', ''))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully.')
            return redirect(next_url or 'MainApp:dashboard')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'mainapp/login.html', {'next_url': next_url})


@login_required
def logout_view(request):
    """Log the user out and return to the marketplace."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('MainApp:skill_list')
