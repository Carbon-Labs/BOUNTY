from django.http import Http404
from django.shortcuts import render

from . import models

def index(request):

    # Generate counts of some of the main objects
    num_projects = models.Project.objects.all().count()
    num_tasks = models.Tasks.objects.all().count()
    num_fundings = models.Fundings.objects.all().count()
    num_projects_goal = (models.Project.objects.all().count() / 10) * 100;
    projects = models.Project.objects.all()[:4]
    featured_projects = models.Project.objects.all().filter(featured=1)

    # Render the HTML template
    return render(
        request,
        'home.html',
        context={'projects': projects, 'featured': featured_projects, 'num_projects':num_projects, 'num_tasks':num_tasks, 'num_fundings':num_fundings, 'num_projects_goal':num_projects_goal},
    )


def project(request, slug):
    try:
        p = models.Project.objects.get(slug=slug)
    except models.Project.DoesNotExist:
        raise Http404("Sorry. That project does not exist")
    return render(
        request,
        'projectdetail.html',
        context={'project': p}
    )
