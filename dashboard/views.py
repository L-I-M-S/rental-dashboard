from django.shortcuts import render, redirect
from django.views import View
from django_chartjs.views import JSONView
from .forms import ExcelUploadForm
from .models import Property, RentPayment
import pandas as pd
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from django.conf import settings

class DashboardView(View):
    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('quickbooks_auth')
        auth_client = AuthClient(
            client_id=settings.QB_CLIENT_ID,
            client_secret=settings.QB_CLIENT_SECRET,
            access_token=request.session.get('access_token'),
            refresh_token=request.session.get('refresh_token'),
            realm_id=request.session.get('realm_id'),
            environment='sandbox'  # Use 'production' for live
        )
        qb = QuickBooks(auth_client=auth_client)
        try:
            invoices = qb.query("SELECT * FROM Invoice")[:10]  # Limit for performance
        except Exception as e:
            invoices = []
        payments = RentPayment.objects.all()
        return render(request, 'dashboard/index.html', {'invoices': invoices, 'payments': payments})

def quickbooks_auth(request):
    auth_client = AuthClient(
        client_id=settings.QB_CLIENT_ID,
        client_secret=settings.QB_CLIENT_SECRET,
        redirect_uri=settings.QB_REDIRECT_URI,
        environment='sandbox'
    )
    url = auth_client.get_authorization_url(scopes=['com.intuit.quickbooks.accounting'])
    return redirect(url)

def quickbooks_callback(request):
    auth_client = AuthClient(
        client_id=settings.QB_CLIENT_ID,
        client_secret=settings.QB_CLIENT_SECRET,
        redirect_uri=settings.QB_REDIRECT_URI,
        environment='sandbox'
    )
    auth_code = request.GET.get('code')
    realm_id = request.GET.get('realmId')
    try:
        token = auth_client.get_bearer_token(auth_code)
        request.session['access_token'] = token.access_token
        request.session['refresh_token'] = token.refresh_token
        request.session['realm_id'] = realm_id
    except Exception as e:
        return render(request, 'dashboard/error.html', {'error': str(e)})
    return redirect('dashboard')

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)
                for _, row in df.iterrows():
                    property_obj, _ = Property.objects.get_or_create(
                        name=row['Property'],
                        defaults={'address': row.get('Address', '')}
                    )
                    RentPayment.objects.create(
                        property=property_obj,
                        tenant=row['Tenant'],
                        amount=row['Amount'],
                        due_date=row['Due Date'],
                        payment_date=row.get('Payment Date', None)
                    )
                return render(request, 'dashboard/upload_success.html')
            except Exception as e:
                return render(request, 'dashboard/error.html', {'error': str(e)})
    else:
        form = ExcelUploadForm()
    return render(request, 'dashboard/upload_excel.html', {'form': form})

class RentChartView(JSONView):
    def get_context_data(self, **kwargs):
        payments = RentPayment.objects.all()
        data = {
            'labels': [p.due_date.strftime('%Y-%m-%d') for p in payments],
            'data': [float(p.amount) for p in payments],
        }
        return {
            'labels': data['labels'],
            'datasets': [{
                'label': 'Rent Collected',
                'data': data['data'],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
            }]
        }
