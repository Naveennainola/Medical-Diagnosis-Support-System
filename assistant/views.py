from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import os
import joblib
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
import csv
from .disease_predictor import predict_disease

from dotenv import load_dotenv

from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
import textwrap

# Load environment variables
load_dotenv()

# Feedback file setup
FEEDBACK_DIR = os.path.join(os.path.dirname(__file__), "dataset")
FEEDBACK_FILE = os.path.join(FEEDBACK_DIR, 'feedback.csv')

if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User_Symptoms", "Predicted_Disease", "Correct_Disease"])

# Load trained model & symptom list
MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
mlb_path = os.path.join(MODEL_DIR, "mlb.pkl")

try:
    mlb = joblib.load(mlb_path)
    symptoms_list = sorted(mlb.classes_)  # Get all available symptoms
    print("✅ Symptoms loaded successfully!")
except Exception as e:
    print(f"❌ Error loading symptoms: {e}")
    symptoms_list = []

# Load CSV files for descriptions & precautions
description_path = os.path.join(os.path.dirname(__file__), "dataset", "disease_Description.csv")
precaution_path = os.path.join(os.path.dirname(__file__), "dataset", "symptom_precaution.csv")
medication_path = os.path.join(os.path.dirname(__file__), 'dataset', "disease_medications_final.csv")

df_description = pd.read_csv(description_path)
df_precaution = pd.read_csv(precaution_path)
df_medication = pd.read_csv(medication_path, header=None)
df_medication.columns = ['Disease','Medications', 'Time-Based Guidance and Preventive Measures']
df_medication = df_medication.columns.str.strip()
# Convert CSVs into dictionaries
disease_descriptions = dict(zip(df_description["Disease"], df_description["Description"]))


disease_precautions = {}
for _, row in df_precaution.iterrows():
    disease = row["Disease"]
    precautions = row.drop("Disease").dropna().tolist()
    disease_precautions[disease] = precautions

def home_view(request):
    return render(request, 'assistant/home.html')

@login_required
def index(request):
    return render(request, 'assistant/index.html', {'symptoms': symptoms_list})

@login_required
def analyze_symptoms(request):
    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").split(",")
        print(symptoms)
        if not symptoms or symptoms == [""]:
            return render(request, "assistant/results.html",
                          {"error": "No symptoms detected. Please enter symptoms."
                        })

        predictions = predict_disease(symptoms)
        print(predictions)
        if "error" in predictions:
            return render(request, "assistant/results.html",
                          {"error": predictions["error"]
                        })

        top_predictions = predictions[:3]
        all_diseases = sorted(df_description['Disease'].unique())


        return render(request, "assistant/results.html", {
            "symptoms": symptoms,
            "predictions": top_predictions,
            "disease_list": all_diseases,
        })

    return redirect('index')


@login_required
def disease_detail_view(request, disease_name):
    desc = disease_descriptions.get(disease_name, "No description found.")
    prec = disease_precautions.get(disease_name, ['No precautions available.'])

    medications, guidance = get_medications_and_guidance(disease_name)

    return render(request, 'assistant/disease_detail.html', {
        'disease_name': disease_name,
        'description': desc,
        'precautions': prec,
        'medications': medications if medications else ['No medications available'],
        'guidance': guidance if guidance else ['No guidance available'],
    })

def submit_feedback(request):
    if request.method == "POST":
        user_symptoms = request.POST.get("symptoms", "")
        predicted_disease = request.POST.get("predicted_disease", "")
        correct_disease = request.POST.get("correct_disease", "")

        if correct_disease and correct_disease != predicted_disease:
            with open(FEEDBACK_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([user_symptoms, predicted_disease, correct_disease])

        return redirect('index')

    return redirect('index')

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        login(request, user)
        return redirect("index")

    return render(request, "assistant/signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'assistant/login.html', {"error": "Invalid username or password"})

    return render(request, 'assistant/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def generate_report(request):
    if request.method == "POST":

        symptoms = request.POST.get('symptoms', '')
        predicted_disease = request.POST.get('predicted_disease', '')
        blood_pressure = request.POST.get('blood_pressure', 'Not provided')
        blood_sugar = request.POST.get('blood_sugar', 'Not provided')
        temperature = request.POST.get('temperature', 'Not provided')
        heart_rate = request.POST.get('heart_rate', 'Not provided')
        spo2 = request.POST.get('spo2', 'Not provided')
        desc = disease_descriptions.get(predicted_disease, 'No description available')

        # Create PDF in memory
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Title Header
        p.setFillColor(colors.HexColor("#2e86de"))
        p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(width / 2, height - 50, "Healthcare Assistant - Medical Report")

        # Draw a line below title
        p.setStrokeColor(colors.grey)
        p.line(50, height - 60, width - 50, height - 60)

        # Section: Prediction
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(colors.black)
        p.drawString(50, height - 100, "Predicted Disease:")
        p.setFont("Helvetica", 12)
        p.drawString(200, height - 100, predicted_disease)

        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, height - 140, 'Disease Description:')
        p.setFont('Helvetica', 12)
        max_width = 90
        wrapped_desc = textwrap.wrap(desc, width=max_width)
        text = p.beginText(70, height - 160)
        text.setLeading(15)
        for line in wrapped_desc:
            text.textLine(line)
        p.drawText(text)



        # Section: Symptoms
        y = text.getY()-20
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Reported Symptoms:")
        p.setFont("Helvetica", 12)
        text = p.beginText(200, y)
        for word in symptoms.split(','):
            text.textLine(word.strip())
        p.drawText(text)

        # Section: Vitals
        y = text.getY() - 20
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Vital Signs:")
        p.setFont("Helvetica", 12)
        vitals = [
            ("Blood Pressure", blood_pressure),
            ("Blood Sugar", blood_sugar),
            ("Temperature", temperature),
            ("Heart Rate", heart_rate),
            ("SpO₂", spo2),
        ]
        y -= 20
        for label, value in vitals:
            p.drawString(70, y, f"{label}:")
            p.drawString(200, y, value)
            y -= 20

        # Footer
        p.setStrokeColor(colors.lightgrey)
        p.line(50, 50, width - 50, 50)
        p.setFont("Helvetica-Oblique", 10)
        p.setFillColor(colors.grey)
        p.drawCentredString(width / 2, 35,
                            "Generated by Healthcare Assistant · Not a substitute for professional medical advice.")

        # Finalize and return
        p.showPage()
        p.save()
        buffer.seek(0)

        return HttpResponse(buffer, content_type='application/pdf', headers={
            'Content-Disposition': 'attachment; filename="medical_report.pdf"'
        })

    return HttpResponse("Invalid Request", status=400)

def get_medications_and_guidance(disease_name):
    csv_path = os.path.join(os.path.dirname(__file__), 'dataset', 'disease_medications_final.csv')
    try:
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()

        # Safety check
        required_cols = ['Disease', 'Medications', 'Time-Based Guidance and Preventive Measures']
        if not all(col in df.columns for col in required_cols):
            return [], []

        filtered = df[df['Disease'].str.lower().str.strip() == disease_name.lower().strip()]

        if filtered.empty:
            return [], []

        row = filtered.iloc[0]  # ✅ safe now
        meds_raw = row['Medications']
        guide_raw = row['Time-Based Guidance and Preventive Measures']

        meds = [m.strip() for m in meds_raw.split(';')] if isinstance(meds_raw, str) else []
        guidance = [g.strip() for g in guide_raw.split(';') if g.strip()] if isinstance(guide_raw, str) else []

        return meds, guidance

    except Exception as e:
        print(f"[ERROR] Failed to load data for {disease_name}: {e}")
        return [], []
