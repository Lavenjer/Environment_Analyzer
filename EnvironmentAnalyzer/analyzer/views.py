from django.shortcuts import render

def home(request):
    context = {
        'title': 'Environment Analyzer Dashboard',
        'status': 'Active',
    }
    return render(request, 'analyzer/index.html', context)
