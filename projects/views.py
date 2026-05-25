import http

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from projects.settings import ProjectStatus, SKILL_AUTOCOMPLETE_LIMIT
from projects.forms import ProjectForm
from projects.models import Project, Skill
from projects.utils import get_paginated_page


def project_list(request):
    """Список проектов по навыку."""
    sel_skill = request.GET.get('skill')

    projects_list = Project.objects.prefetch_related('skills', 'participants').order_by('-created_at')

    if sel_skill:
        projects_list = projects_list.filter(skills__name=sel_skill).distinct()

    projects = get_paginated_page(request, projects_list)
    all_skills = Skill.objects.values_list('name', flat=True).distinct().order_by('name')

    context = {
        'projects': projects,
        'all_skills': all_skills,
        'active_skill': sel_skill,
    }
    return render(request, 'projects/project_list.html', context)


@login_required
def project_create(request):
    """Создание нового проекта"""
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:detail', pk=project.pk)

    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, 'projects/create-project.html',context)


@login_required
def project_edit(request, pk):
    """Изменить проект"""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect('projects:detail', pk=project.pk)

    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, 'projects/create-project.html',context)


def project_detail(request, pk):
    """Страница проекта"""
    project = get_object_or_404(Project.objects.prefetch_related('skills', 'participants'), pk=pk)

    context = {'project': project,
                'skills': project.skills.all(),
                'participants': project.participants.all()}
    return render(request, 'projects/project-details.html',context)


@login_required
def join_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user == project.owner:
        return redirect('projects:detail', pk=pk)

    if project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return redirect('projects:detail', pk=pk)


def skill_autocomplete(request):
    if query := request.GET.get('q', ''):
        skills = Skill.objects.filter(name__icontains=query)[:SKILL_AUTOCOMPLETE_LIMIT]
        results = [{'id': s.id, 'name': s.name} for s in skills]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


@login_required
@require_POST
def toggle_project_status(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    project.status = (
        ProjectStatus.CLOSED if project.status == ProjectStatus.OPEN
        else ProjectStatus.OPEN
    )
    project.save()
    return JsonResponse({'status': 'ok', 'new_status': project.get_status_display()})


@login_required
@require_POST
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if is_in_favs := project.favorited_by.filter(id=request.user.id).exists():
        project.favorited_by.remove(request.user)
    else:
        project.favorited_by.add(request.user)

    return JsonResponse({'status': 'ok', 'is_favorite': not is_in_favs})


@login_required
@require_POST
def add_skill_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if skill_name := request.POST.get('name', '').strip():
        skill, _ = Skill.objects.get_or_create(name=skill_name)
        project.skills.add(skill)
        return JsonResponse({'id': skill.id, 'name': skill.name, 'status': 'ok'})

    return JsonResponse({'status': 'error'}, status=http.HTTPStatus.BAD_REQUEST)


@login_required
@require_POST
def remove_skill_from_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if skill_id := request.POST.get('skill_id'):
        skill = get_object_or_404(Skill, id=skill_id)
        project.skills.remove(skill)
        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'}, status=http.HTTPStatus.BAD_REQUEST)


def redirect_to_projects(request):
    return redirect('projects:list')

