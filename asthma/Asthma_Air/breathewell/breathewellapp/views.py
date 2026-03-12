from django.shortcuts import render,redirect,HttpResponse
from urllib3 import request
from . import models
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword ')
        image = request.FILES.get('image')
        allergies = request.POST.get('allergies')
        medicalconditions = request.POST.get('medicalconditions')
        alertthreshold = request.POST.get('alertthreshold')
        notificationmethod = request.POST.get('notificationmethod')

        if Register.objects.filter(email=email).exists():
           alert="<script>alert('Email already exists!');window.location.href='/register/';</script>;"
           return HttpResponse(alert)
        
        else:
            user = Register(username=username,age=age,gender=gender,email=email,phone=phone,address=address,password=password,confirmpassword =confirmpassword ,image=image,allergies=allergies,medicalconditions=medicalconditions,alertthreshold=alertthreshold,notificationmethod=notificationmethod)
            user.save()
            return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Register.objects.get(email=email)

            if user.password == password:
                request.session['email'] = email
                return redirect('userhome')
            else:
                return HttpResponse("<script>alert('Invalid email or password!');window.location.href='/login/';</script>;")
            
        except Register.DoesNotExist:
            return HttpResponse("<script>alert('User Not Found!');window.location.href='/login/';</script>;")
        
    return render(request, 'login.html')


def personal(request):
    return render(request, 'personal.html')

def userhome(request):
    return render(request, 'userhome.html')

def logout(request):
    request.session.flush()
    return redirect('index')

def profile(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = Register.objects.get(email=email)
            return render(request, 'profile.html', {'user': user})

        except Register.DoesNotExist:
            return HttpResponse("<script>alert('User Not Found!');window.location.href='/login/';</script>;")
        
    return redirect('login')


def editprofile(request):
    if 'email' in request.session:
        email = request.session['email']

        try:
            user = Register.objects.get(email=email)

            if request.method == 'POST':
                user.username = request.POST.get('username')
                user.age = request.POST.get('age')
                user.gender = request.POST.get('gender')
                user.email = request.POST.get('email')
                user.phone = request.POST.get('phone')
                user.address = request.POST.get('address')
                user.image = request.FILES.get('image', user.image)
                user.allergies = request.POST.get('allergies')
                user.medicalconditions = request.POST.get('medicalconditions')
                user.alertthreshold = request.POST.get('alertthreshold')
                user.notificationmethod = request.POST.get('notificationmethod')
                user.save()
                return HttpResponse("<script>alert('Profile updated successfully!');window.location.href='/profile/';</script>;")

            return render(request, 'editprofile.html', {'user': user})

        except Register.DoesNotExist:
            return HttpResponse("<script>alert('User Not Found!');window.location.href='/login/';</script>;")

    return redirect('login')    







from django.shortcuts import render
from .models import SensorData

def realtimedata(request):
    data = SensorData.objects.using('mysql_db').latest('id')

    # -------------------------
    # Convert all sensor values
    # -------------------------
    room_temp = float(data.value1)
    humidity = float(data.value2)
    body_temp = float(data.value3)
    heart_rate = int(float(data.value4))
    spo2 = int(float(data.value5))
    air_quality = data.value7

    advisories = []
    risk_level = "Low"
    risk_class = "low"

    # Room Temperature
    if room_temp < 18:
        advisories.append("Room temperature is low. Consider warming the environment.")
    elif room_temp > 30:
        advisories.append("Room temperature is high. Ensure proper cooling and ventilation.")

    # Humidity
    if humidity < 30:
        advisories.append("Low humidity detected. Dry air may cause discomfort.")
    elif humidity > 60:
        advisories.append("High humidity detected. Ventilation is recommended.")

    # Body Temperature
    if body_temp < 36:
        advisories.append("Body temperature is below normal. Keep warm and monitor.")
        risk_level, risk_class = "Medium", "medium"
    elif body_temp > 37.5:
        advisories.append("Elevated body temperature detected. Rest and monitor closely.")
        risk_level, risk_class = "Medium", "medium"

    # Heart Rate
    if heart_rate < 60:
        advisories.append("Heart rate is lower than normal. Monitor for symptoms.")
        risk_level, risk_class = "Medium", "medium"
    elif heart_rate > 100:
        advisories.append("High heart rate detected. Rest immediately.")
        risk_level, risk_class = "High", "high"

    # SpO2
    if spo2 < 90:
        advisories.append("Critical oxygen level detected. Seek medical attention.")
        risk_level, risk_class = "High", "high"
    elif spo2 < 95 and risk_level != "High":
        advisories.append("Slightly low oxygen level. Rest and breathe deeply.")
        risk_level, risk_class = "Medium", "medium"

    if not advisories:
        advisories.append("All readings are within normal range. Stay healthy!")

    context = {
        'value1': room_temp,
        'value2': humidity,
        'value3': body_temp,
        'value4': heart_rate,
        'value5': spo2,
        'value7': air_quality,
        'risk_level': risk_level,
        'risk_class': risk_class,
        'advisories': advisories,
    }

    return render(request, 'realtimedata.html', context)





from django.shortcuts import render
from .models import RiskPrediction

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def risklevels(request):
    if request.method == "POST":
        pm25 = float(request.POST.get('pm25'))
        co = float(request.POST.get('co'))
        heart_rate = int(request.POST.get('heartRate'))
        spo2 = int(request.POST.get('spo2'))

        # -------------------------------
        # RULE-BASED LOGIC (EXECUTES)
        # -------------------------------
        risklevel = "Low"
        advisory = "Your health risk is low."

        if pm25 > 55 or co > 10 or spo2 < 93 or heart_rate > 95:
            risklevel = "High"
            advisory = "High health risk detected!"
        elif pm25 > 35 or co > 6 or spo2 < 95 or heart_rate > 85:
            risklevel = "Medium"
            advisory = "Moderate health risk."


        try:
            raise Exception("Skip ML execution")
        except:
            train_qs = RiskPrediction.objects.all().values(
                'pm25', 'co', 'heart_rate', 'spo2', 'risk_level'
            )
            df = pd.DataFrame(list(train_qs))
            if not df.empty:
                le = LabelEncoder()
                df['risk_encoded'] = le.fit_transform(df['risk_level'])

                X = df[['pm25', 'co', 'heart_rate', 'spo2']]
                y = df['risk_encoded']

                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X, y)

                prediction = model.predict([[pm25, co, heart_rate, spo2]])

        # -------------------------------
        # SAVE RESULT
        # -------------------------------
        RiskPrediction.objects.create(
            pm25=pm25,
            co=co,
            heart_rate=heart_rate,
            spo2=spo2,
            risk_level=risklevel,
            advisory=advisory
        )

        return render(request, 'risklevels.html', {
            'risklevel': risklevel,
            'advisory': advisory
        })

    return render(request, 'risklevels.html')



# views.py
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import SensorData

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import SensorData

def historicaldata(request):
    now = timezone.now()

    # Last 7 days
    last_7_days = SensorData.objects.using('mysql_db').filter(
        reading_time__gte=now - timedelta(days=7)
    ).order_by('reading_time')

    # Last 30 days
    last_30_days = SensorData.objects.using('mysql_db').filter(
        reading_time__gte=now - timedelta(days=30)
    ).order_by('reading_time')

    context = {
        'labels_7': [d.reading_time.strftime('%Y-%m-%d %H:%M') for d in last_7_days],
        'pm25_7': [d.value1 for d in last_7_days],
        'hr_7': [d.value2 for d in last_7_days],

        'labels_30': [d.reading_time.strftime('%Y-%m-%d') for d in last_30_days],
        'pm25_30': [d.value1 for d in last_30_days],
        'hr_30': [d.value2 for d in last_30_days],
    }

    return render(request, 'historicaldata.html', context)



@login_required
def historicaldataapi(request, timeframe):
    """
    Return historical data as JSON for Chart.js
    timeframe: '24hr', '7day', '30day'
    """
    user = request.user
    endtime = now()

    if timeframe == '24hr':
        start_time = endtime - timedelta(hours=24)
    elif timeframe == '7day':
        start_time = endtime - timedelta(days=7)
    elif timeframe == '30day':
        start_time = endtime - timedelta(days=30)
    else:
        return JsonResponse({'error': 'Invalid timeframe'}, status=400)

    data_qs = HistoricalData.objects.filter(user=user, timestamp__range=(start_time, endtime)).order_by('timestamp')

    labels = [entry.timestamp.strftime('%Y-%m-%d %H:%M') for entry in data_qs]
    pm25 = [entry.pm25 for entry in data_qs]
    heart_rate = [entry.heart_rate for entry in data_qs]

    return JsonResponse({
        'labels': labels,
        'pm25': pm25,
        'heart_rate': heart_rate,
    })



from django.shortcuts import render
from .models import PollutedData

def routeoptimization(request):
    polluted_places = PollutedData.objects.all().values(
        'place_name', 'latitude', 'longitude', 'radius'
    )
    return render(request, 'routeoptimization.html', {
        'polluted_places': list(polluted_places)
    })



def about(request):
    user = Register.objects.all()
    return render(request, 'about.html', {'users': user})


import pandas as pd
import numpy as np
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import SensorData
from .utils import arima_forecast  # Your ARIMA helper

def forecast(request):
    now = timezone.now()

    # Fetch last 30 days of data
    qs = SensorData.objects.using('mysql_db').filter(
        reading_time__gte=now - timedelta(days=30)
    ).order_by('reading_time')

    if not qs.exists():
        return render(request, 'forecast.html', {'error': 'No data available'})

    # Convert to DataFrame
    df = pd.DataFrame.from_records(qs.values(
        'reading_time', 'value1', 'value2', 'value3', 'value4', 'value5'
    ))

    # Convert to datetime and set index
    df['reading_time'] = pd.to_datetime(df['reading_time'])
    df.set_index('reading_time', inplace=True)

    # Ensure numeric columns
    for col in ['value1', 'value2', 'value3', 'value4', 'value5']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop missing rows
    df.dropna(inplace=True)

    if len(df) < 20:
        return render(request, 'forecast.html', {'error': 'Not enough data for forecasting'})

    # Forecast periods: next 1 day and next 7 days
    steps_1d = 24  # assuming 1 reading per hour
    steps_7d = 24 * 7

    # ARIMA forecast
    forecast_temp_1d = arima_forecast(df['value1'], steps_1d)
    forecast_temp_7d = arima_forecast(df['value1'], steps_7d)

    forecast_hum_1d = arima_forecast(df['value2'], steps_1d)
    forecast_hum_7d = arima_forecast(df['value2'], steps_7d)

    forecast_bodytemp_1d = arima_forecast(df['value3'], steps_1d)
    forecast_bodytemp_7d = arima_forecast(df['value3'], steps_7d)

    forecast_bpm_1d = arima_forecast(df['value4'], steps_1d)
    forecast_bpm_7d = arima_forecast(df['value4'], steps_7d)

    forecast_spo2_1d = arima_forecast(df['value5'], steps_1d)
    forecast_spo2_7d = arima_forecast(df['value5'], steps_7d)


    # Generate future timestamps
    last_time = df.index[-1]
    future_1d = [last_time + timedelta(hours=i+1) for i in range(steps_1d)]
    future_7d = [last_time + timedelta(hours=i+1) for i in range(steps_7d)]

    # Combine historical + forecast for template
    context = {
        'labels': df.index.strftime('%Y-%m-%d %H:%M').tolist(),
        'hist_len': len(df),
        'temp': df['value1'].tolist(),
        'hum': df['value2'].tolist(),
        'bodytemp': df['value3'].tolist(),
        'bpm': df['value4'].tolist(),
        'spo2': df['value5'].tolist(),

        'forecast_labels_1d': [t.strftime('%Y-%m-%d %H:%M') for t in future_1d],
        'forecast_labels_7d': [t.strftime('%Y-%m-%d %H:%M') for t in future_7d],

        'f_temp_1d': forecast_temp_1d.tolist(),
        'f_temp_7d': forecast_temp_7d.tolist(),

        'f_hum_1d': forecast_hum_1d.tolist(),
        'f_hum_7d': forecast_hum_7d.tolist(),

        'f_bodytemp_1d': forecast_bodytemp_1d.tolist(),
        'f_bodytemp_7d': forecast_bodytemp_7d.tolist(),

        'f_bpm_1d': forecast_bpm_1d.tolist(),
        'f_bpm_7d': forecast_bpm_7d.tolist(),

        'f_spo2_1d': forecast_spo2_1d.tolist(),
        'f_spo2_7d': forecast_spo2_7d.tolist(),
    }

    return render(request, 'forecast.html', context)
