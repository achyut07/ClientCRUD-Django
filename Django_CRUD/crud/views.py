from django.shortcuts import render, redirect, HttpResponse

from .models import ClientList

# Create your views here.

def index(request):
    clients = ClientList.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'index.html', context)

def create(request):
    print(request.POST.get)
    client_name = request.GET['client_name']
    client_company = request.GET['client_company']
    company_location = request.GET['company_location']
    company_logo = request.GET['company_logo']
    contactno = request.GET['contactno']
    project_name = request.GET['project_name']
    tools = request.GET['tools']
    offer_date = request.GET['offer_date']
    deadline = request.GET['deadline']
    
    client_details = ClientList(client_name=client_name, client_company=client_company, company_location=company_location,\
     company_logo=company_logo,contactno=contactno, project_name=project_name, tools=tools, offer_date=offer_date, deadline=deadline)
     
    client_details.save()
    return redirect('/')


def add_client(request):
    return render(request, 'add_client.html')



def delete(request, id):
    clients = ClientList.objects.get(pk=id)
    clients.delete()
    return redirect('/')

def edit(request, id):
    clients = ClientList.objects.get(pk=id)
    context = {
        'clients': clients
    }
    return render(request, 'edit.html', context)


def update(request, id):
    clients = ClientList.objects.get(pk=id)
    clients.client_name = request.GET['client_name']
    clients.client_company = request.GET['client_company']
    clients.company_location = request.GET['company_location']
    clients.company_logo= request.GET['company_logo']
    clients.contactno = request.GET['contactno']
    clients.project_name = request.GET['project_name']
    clients.offer_date = request.GET['offer_date']
    clients.deadline = request.GET['deadline']
    clients.save()
    return redirect('/')

