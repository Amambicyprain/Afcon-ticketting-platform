import random
from afcon.settings import EMAIL_HOST_USER
from django.core import paginator
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from ticket_sales.models import *
from django.urls import reverse
from datetime import date
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from qr_code.qrcode.utils import ContactDetail, WifiConfig, Coordinates, QRCodeOptions
from campay.sdk import Client
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from weasyprint import HTML
import tempfile
import os
import uuid
from django.contrib import messages

numbers=['01','02','03','04','05','06','07','08','09']

campay = Client({
    "app_username" : "UPsdL44n9oLAFYvd0bo-D-Lqf3YATVPysl8xBRIIj23Gu4XkXj0NfW77sUOe4tWFJ2GGSZKHgUSphVJjvLRapg",
    "app_password" : "ZxX8_JlxxSjKqkUvM3Id9Vq78xu8KHhtl7wfWeljoMran1EChrOYkZWGs_LY30-9E71ZdLbAakWIRe7-a9fYhA",
    "environment" : "DEV" #use "DEV" for demo mode or "PROD" for live mode
})

# Create your views here.
# home page #
def index(request):
    upcoming_matches = Match.objects.all().order_by('match_time').filter(match_time__gte = timezone.now())[:3]
    # print(upcoming_matches)
    # for match in upcoming_matches:
    #     image = match.match_staduim.Staduim_image
    #     print(image.url)
    context = {
        'upcoming_matches': upcoming_matches
    }
    return render(request,'index.html',context=context)


# home page #
# list of matches # 
def matches(request):
    matches = Match.objects.all().order_by('match_time')
    paginator = Paginator(matches,6)
    page_number = request.GET.get('page')
    matches = paginator.get_page(page_number)

    context ={
        'matches':matches
    }
    return render(request,'matches.html',context=context)
# list of matches # 

def staduim_detail(request,id):
    staduim = get_object_or_404(Staduim,id = id)
    matches = staduim.match_set.all()
    context = {
        'staduim' : staduim,
        'matches' : matches,
    }
    return render(request,'matches.html',context)
    

# list of sales #
def sales(request):
    sales = Sales.objects.all().order_by('sales_date')
    context = {
        'sales': sales
    }
    return render(request,'sales.html',context=context)


def search_match(request):
        urser = request.user
        if request.POST:
            searched_name = request.POST['searched_word']
            match_gotten = Match.objects.filter(home_team__team_name__icontains = searched_name) | Match.objects.filter(away_team__team_name__icontains = searched_name)
            print(match_gotten)
            staduims_gotten = Staduim.objects.filter(staduim_name__contains = searched_name)
            print(staduims_gotten)
            for staduim in staduims_gotten:
                match_gotten = match_gotten.union(match_gotten,staduim.match_set.all())
            print(match_gotten)
            matches = match_gotten
            paginator = Paginator(matches,6)
            page_number = request.GET.get('page')
            matches = paginator.get_page(page_number)

            context ={
            'matches': matches
            }
            return render (request, 'search_result.html',context = context)
# list of sales # 

# def ticket(request):
#     match = Match.objects.get(id=2)
#     customer= Customer.objects.get(id =1)
#     customer_name = customer.customer_first_name +'   ' + customer.customer_last_name

#     print(match)
#     context={
#     'match':match,
#     'customer_name':customer_name,
#     'customer':customer,
#     }
#     return render (request, 'ticket.html', context=context)

def payment_page(request):
    # match=get_object_or_404(Match,id=match_id)
    # context={
    # 'match':match
    # }
    return render(request, 'base.html', {})

def buy_ticket(request, match_id):
    
    match=get_object_or_404(Match,id=match_id)
    context = {
    'match_id' : match_id 
    }

    #Check if the post has been sent before or if it's the first time
    if request.method == 'POST':
        destination = reverse('home_page')
        rebuy = request.POST.get('buy_more',False)
        if rebuy:
            destination = request.path

        match=get_object_or_404(Match,id=match_id)
        print(match.id)
        print(match)
        new_customer = Customer(
            customer_first_name = request.POST['f_name'],
            customer_last_name  = request.POST['l_name'],
            customer_email      = request.POST['email'],
            customer_phone      = request.POST['phone_number'],
            customer_idcard     = request.POST['id'],
        )
        new_customer.save()
        new_ticket = Tickets(
            ticket_category = request.POST['ticket_category'],
            ticket_name = 'TICKET'+str(random.randint(0,49)),
            ticket_match = match
        )
        new_ticket.save()

        new_sale=Sales()
        new_sale.sales_name = 'SALE'+str(random.randint(0,49))
        new_sale.sales_date = date.today()
        new_sale.sales_customer = new_customer
        new_sale.sales_ticket = new_ticket

       
        phone_number = new_customer.customer_phone
        amount = request.POST['ticket_cost']
        print(amount)
            #Collecting payments using campay
            # collect = campay.collect({
            #     "amount": str(amount), #The amount you want to collect
            #     "currency": "XAF",
            #     "from": ("237"+str(phone_number)), #Phone number to request amount from. Must include country code
            #     "description": "Ticket Payment for the "+ match.match_name + " " + match.match_round + "match"
            # })
            # if collect.get("status") == 'SUCCESSFUL':
            #     new_sale.save()
        messages.success(request, 'You have successfully bought your ticket')
        qr =gen_qrcode(customer=new_customer)
        export_pdf(request,qr,customer=new_customer,match=match,ticket_category =new_ticket.ticket_category)
        
        mail = EmailMessage(
        'Afcon Ticketting platform',#Subject
        'Congratulations you have successfully aquired your ticket. Attached is the E-copy',#Message
        EMAIL_HOST_USER,#from
        [new_customer.customer_email],#to
        )
        mail.attach_file('ticket_sales/report.pdf')
        mail.send(fail_silently=False,)#no clue
        # print(mail.send(fail_silently=False,))
            
        return redirect(destination)
    return render(request, 'payment_form.html', context)
            
 

def staduims(request):
    staduims = Staduim.objects.all()
    print(staduims)
    context ={
        'staduims': staduims
    }
    return render(request, 'staduim.html' ,context = context)

def generate_pdf():
    pass

def generate_pdf_from_template(request):
   

    html = render_to_string('ticket.html',context)
    
    write_to_file = open('media/test_2.pdf', "w+b")
    
    result = pisa.CreatePDF(html,dest=write_to_file)
    
    write_to_file.close()
    
    # return HttpResponse(result.err)
    return redirect(reverse('home_page'))

def render_pdf(request):
    path = "payment_form.html"
    context = {"matches" : Match.objects.all()[:4]}

    html = render_to_string(path,context)
    io_bytes = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/afcon')

dirname = os.path.dirname(__file__)


def export_pdf(request,qr,customer,match,ticket_category):
    customer_name = customer.customer_first_name +'   ' + customer.customer_last_name
    context={
    'match':match,
    'customer_name':customer_name,
    'qr': qr,
    'customer':customer,
    'ticket_category':ticket_category,
    }
    context.update(qr)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string =  html = render_to_string('ticket.html',context)
    html = HTML(string= html_string,base_url=request.build_absolute_uri())
    result = html.write_pdf()
    if os.path.exists(dirname):

        f = open(os.path.join(dirname, 'report.pdf'), 'wb')
        f.write(result)

    with tempfile.NamedTemporaryFile(delete = True) as output :
        output.write(result)
        output.flush()
        output = open(output.name,'rb')
        response.write(output.read())
    return response

def delete_file():
    fs= FileSystemStorage()
    fs.delete(os.path.join(MEDIAROOT,'report.pdf'))

def gen_qrcode(customer):
    rand = uuid.uuid4().hex[:8]
    rand_id = rand
    rand = str(rand) +' ' + customer.customer_first_name + ' ' + customer.customer_last_name
    context = {
    'my_options' : QRCodeOptions(size='t',border = 6, error_correction = 'L'),
    'rand':rand,
    'rand_id': rand_id,
    }
    return context