from uuid import uuid4
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

from peacecorps.forms import DedicationForm, IndividualDonationForm
from peacecorps.forms import OrganizationDonationForm


def donation_payment_individual(request):
    """ This is the view for the donations contact information form. """
    if request.method == 'POST':
        form = IndividualDonationForm(request.POST)
        dedication_form = DedicationForm(request.POST)

        if form.is_valid():
            for k,v in form.cleaned_data.items():
                request.session[k] = v
            return HttpResponseRedirect('/donations/review')
    else:
        form = IndividualDonationForm()
        dedication_form = DedicationForm()
    return render(request, 'donations/donation_payment.jinja',
        {'form': form, 'dedication_form': dedication_form})

def donation_payment_organization(request):
    if request.method == 'POST':
        form = OrganizationDonationForm(request.POST)
        dedication_form = DedicationForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/donations/review')
    else:
        form = OrganizationDonationForm(initial={'donor_type':'Organization'})
        dedication_form = DedicationForm()
    return render(request, 'donations/donation_payment.jinja',
        {   
            'form': form,
            'organization': True,
            'dedication_form': dedication_form 
        })

def generate_agency_tracking_id():
    """ Generate an agency tracking ID for the transaction that has some random
    component. I include the date in here too, in case that's useful. (The
    current non-random tracking id has the date in it. """

    random = str(uuid4()).replace('-', '')
    today = datetime.now().strftime("%m%d")
    return 'PCIOCI%s%s' % (today, random[0:6]) 

def generate_agency_memo(data):
    """ This currently returns a faked agency memo. Later we'll replace this.
    """

    return '()(14-491-001, $10.00/)(%s)(yes)(no)(yes)' % data['phone_number']

def donation_payment_review(request):
    data = {}
    for k,v in request.session.items():
        data[k] = v
    
    return render(
        request,
        'donations/review_payment.jinja',
        {
            'data': data,
            'agency_memo': generate_agency_memo(data),
            'agency_id': settings.PAY_GOV_AGENCY_ID,
            'tracking_id': generate_agency_tracking_id(),
            'app_name': settings.PAY_GOV_APP_NAME,
            'oci_servlet_url': settings.PAY_GOV_OCI_URL,
        })
