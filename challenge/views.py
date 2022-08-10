from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from django.core.paginator import Paginator
import io, os, random, xmltodict, requests
from challenge.models import ForexConvert
from challenge.serializers import ForexSerializer
from sqlalchemy import create_engine
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

current_path = os.getcwd()
app_path = os.path.join(current_path, 'static')

# Function to upload the file and parse the file to database

def home_file_upload(request):
    # Checks the request method type
    if request.method == 'POST':
        uploaded_file = request.FILES['document']

        # Checks the file type to process accodingly
        if uploaded_file.name.endswith(".csv"):
            decoded_file = io.StringIO(uploaded_file.read().decode('utf-8'))
            df = pd.read_csv(decoded_file, sep=r'[:,|_]', engine='python')
            df = df.iloc[: , 1:]
            
        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
            df = df.iloc[: , 1:]
            
        elif uploaded_file.name.endswith(".xml"):
            data = xmltodict.parse(uploaded_file)
            df = pd.DataFrame(data['root']['element'])

        # Make headers consistent for all types and calculate amount after conversion
        df.columns = ['SourceCurrency', 'DestinationCurrency', 'SourceAmount']    
        df['DestinationAmount'] = round(df.apply(lambda x: map_conversion_rate(x.SourceCurrency.strip(), x.DestinationCurrency.strip(), x.SourceAmount), axis=1),2)
        # print(df.head())
        
        # Stores the processed data into the database forex.sqlite3
        engine = create_engine('sqlite:///forex.sqlite3')
        df.to_sql(ForexConvert._meta.db_table, if_exists='replace', con=engine, index=False)
        messages.success(request, 'Form submission successful')
        return redirect(display_result)
        # return render(request, "home.html")

    return render(request, "home.html")

# Map conversion rate for all possibilities
def map_conversion_rate(source,convert_to,amount):
    conversion_data = {
        'GBP:USD':fetch_conversion_rate('GBP','USD'),
        'GBP:EUR':fetch_conversion_rate('GBP','EUR'),
        'GBP:AUD':fetch_conversion_rate('GBP','AUD'),
        'USD:GBP':fetch_conversion_rate('USD','GBP'),
        'USD:EUR':fetch_conversion_rate('USD','EUR'),
        'USD:AUD':fetch_conversion_rate('USD','AUD'),
        'EUR:USD':fetch_conversion_rate('EUR','USD'),
        'EUR:GBP':fetch_conversion_rate('EUR','GBP'),
        'EUR:AUD':fetch_conversion_rate('EUR','AUD'),
        'AUD:USD':fetch_conversion_rate('AUD','USD'),
        'AUD:EUR':fetch_conversion_rate('AUD','EUR'),
        'AUD:GBP':fetch_conversion_rate('AUD','GBP')
    }
    # print(amount,conversion_data.get(f'{source}:{convert_to}'))

    return amount*conversion_data.get(f'{source}:{convert_to}')

# Fetch conversion rate from the api or assign random value if unable to access api
def fetch_conversion_rate(CurrencyFrom,CurrencyTo):

    #API details to fetch the conversion rate
    url = "https://api.apilayer.com/fixer/convert?to="+CurrencyTo+"&from="+CurrencyFrom+"&amount=10"

    payload = {}
    headers= {
    "apikey": "3aRhIQO7e9kuz38Kl25ikYf53BzUWc1j"
    }
    
    response = requests.request("GET", url, headers=headers, data = payload)

    if response.status_code == '200':
        response = response.json()
        return response['info']['rate']
    else:
        return random.random()

# Fetch data from database and display result
def display_result(request):
    forex_list = list(ForexConvert.objects.all().values('SourceCurrency', 'DestinationCurrency', 'SourceAmount', 'DestinationAmount')) 
    paginator = Paginator(forex_list, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # print(forex_list, page_obj)

    return render(request, 'result.html', {'page_obj':page_obj})

# Implemented REST Framework to get data from database using any frontend application
@csrf_exempt
def forexApi(request):
    if request.method == 'GET':
        forex_api_obj = ForexConvert.objects.all().values('SourceCurrency', 'DestinationCurrency', 'SourceAmount', 'DestinationAmount')
        forex_serializer = ForexSerializer(forex_api_obj, many=True)
        return JsonResponse(forex_serializer.data, safe=False)
    
    pass

