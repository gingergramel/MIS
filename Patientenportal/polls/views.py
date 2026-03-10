from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model

from polls.forms import DiseaseForm
from .models import Disease, Patient, Practitioner, Questionnaire, Message

User = get_user_model()

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        # Überprüfen, ob der User ein Practitioner ist
        try:
            practitioner = Practitioner.objects.get(user=request.user)
            context['is_practitioner'] = True
            context['show_questionnaire_button'] = False
        except Practitioner.DoesNotExist:
            context['is_practitioner'] = False
            # wenn Patient, prüfen ob Fragebogen existiert
            try:
                patient = Patient.objects.get(user=request.user)
                context['show_questionnaire_button'] = not hasattr(patient, 'questionnaire')
            except Patient.DoesNotExist:
                context['show_questionnaire_button'] = False
    return render(request, 'home.html', context=context)


def patient_login(request):
    login_status = ""
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                patient = Patient.objects.get(user=user)
                login(request, user)
                # Prüfe, ob Fragebogen existiert
                if not hasattr(patient, 'questionnaire'):
                    return redirect('questionnaire')
                return redirect('/')
            except Patient.DoesNotExist:
                login_status = "FAILURE"
        else:
            login_status = "FAILURE"
    return render(request, 'patient_login.html', context={'login_status': login_status})


def practitioner_login(request):
    login_status = ""
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Überprüfen, ob der User ein Practitioner ist
            try:
                practitioner = Practitioner.objects.get(user=user)
                login(request, user)
                return redirect('/')
            except Practitioner.DoesNotExist:
                login_status = "FAILURE"
        else:
            login_status = "FAILURE"

    return render(request, 'practitioner_login.html', context={'login_status': login_status})


def perform_logout(request):
    logout(request)
    return redirect('/')


def perform_register(request):
    registration_status = ""
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        try:
            if User.objects.filter(username=username).exists():
                registration_status = "USERNAME_TAKEN"
            else:
                User.objects.create_user(username=username, password=password)
                registration_status = "SUCCESS"
        except Exception:
            registration_status = "FAILURE"

        return render(request, 'register.html', context={'registration_status': registration_status})

    return render(request, 'register.html', context={'registration_status': registration_status})


def patient_register(request):
    registration_status = ""
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        password = request.POST.get("password", "")
        svnr = request.POST.get("SVNR", "")
        geburtsdatum = request.POST.get("Geburtsdatum", "")
        if User.objects.filter(username=username).exists():
            registration_status = "Username bereits vergeben."
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()
            Patient.objects.create(user=user, insurance_number=svnr, date_of_birth=geburtsdatum, address="", phone_number="")
            registration_status = "Registrierung erfolgreich! Dein Account muss vom Admin freigeschaltet werden."
    return render(request, 'patient_register.html', {"registration_status": registration_status})


def practitioner_register(request):
    registration_status = ""
    PRACTITIONER_KEY = "Hallo_Servus_123"  # Beispiel-Schlüssel, in der Praxis sicherer handhaben
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        fachrichtung = request.POST.get("Fachrichtung", "")
        lizenznummer = request.POST.get("Lizenznummer", "")
        register_key = request.POST.get("register_key", "")
        if register_key != PRACTITIONER_KEY:
            registration_status = "Falscher Registrierungsschlüssel!"
        elif User.objects.filter(username=username).exists():
            registration_status = "Username bereits vergeben."
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Practitioner.objects.create(user=user, specialization=fachrichtung, license_number=lizenznummer, office_hours="", is_admin=False)
            login(request, user)  # Log the user in automatically
            return redirect('/')
    return render(request, 'practitioner_register.html', {"registration_status": registration_status})


def questionnaire(request):
    if not request.user.is_authenticated:
        return redirect('patient_login')
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return redirect('patient_login')
    # allow creating or editing the questionnaire
    questionnaire = getattr(patient, 'questionnaire', None)
    status = ""
    if request.method == "POST":
        main_complaint = request.POST.get('main_complaint', '')
        pain_duration = request.POST.get('pain_duration', '')
        pain_frequency = request.POST.get('pain_frequency', '')
        pain_intensity = request.POST.get('pain_intensity', '')
        previous_treatment = request.POST.get('previous_treatment', '')
        
        if questionnaire is None:
            Questionnaire.objects.create(
                patient=patient,
                main_complaint=main_complaint,
                pain_duration=pain_duration,
                pain_frequency=pain_frequency,
                pain_intensity=pain_intensity,
                previous_treatment=previous_treatment
            )
        else:
            questionnaire.main_complaint = main_complaint
            questionnaire.pain_duration = pain_duration
            questionnaire.pain_frequency = pain_frequency
            questionnaire.pain_intensity = pain_intensity
            questionnaire.previous_treatment = previous_treatment
            questionnaire.save()
        return redirect('patient_dashboard')

    # GET: show form, prefill if questionnaire exists
    return render(request, 'questionnaire.html', {'status': status, 'questionnaire': questionnaire})


def patient_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('patient_login')
    try:
        patient = Patient.objects.get(user=request.user)
        practitioner = patient.practitioner
    except Patient.DoesNotExist:
        return redirect('patient_login')
    return render(request, 'patient_dashboard.html', {'practitioner': practitioner})


def practitioner_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('practitioner_login')
    try:
        practitioner = Practitioner.objects.get(user=request.user)
    except Practitioner.DoesNotExist:
        return redirect('practitioner_login')
    patients = Patient.objects.filter(practitioner=practitioner)
    patient_data = []
    for patient in patients:
        questionnaire = getattr(patient, 'questionnaire', None)
        # unread messages for practitioner = messages sent by patient and not yet read by practitioner
        unread_messages = Message.objects.filter(
            patient=patient,
            practitioner=practitioner,
            sender_is_practitioner=False,
            read_by_practitioner=False
        ).count()
        patient_data.append({
            'patient': patient,
            'questionnaire': questionnaire,
            'unread_messages': unread_messages
        })
    return render(request, 'practitioner_dashboard.html', {'patient_data': patient_data})

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('patient_login')
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return redirect('patient_login')

    if request.method == "POST":
        # Update user data
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        # Update patient data
        patient.date_of_birth = request.POST.get('date_of_birth')
        patient.address = request.POST.get('address')
        patient.phone_number = request.POST.get('phone_number')
        patient.insurance_number = request.POST.get('insurance_number')
        patient.save()

        return render(request, 'edit_profile.html', {
            'user': request.user,
            'patient': patient,
            'status': 'Daten erfolgreich aktualisiert!'
        })

    return render(request, 'edit_profile.html', {
        'user': request.user,
        'patient': patient
    })

def patient_messages(request):
    if not request.user.is_authenticated:
        return redirect('patient_login')
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return redirect('patient_login')

    if not patient.practitioner:
        return redirect('patient_dashboard')

    if request.method == "POST":
        message_content = request.POST.get('message')
        if message_content:
            # create message from patient to practitioner
            Message.objects.create(
                patient=patient,
                practitioner=patient.practitioner,
                content=message_content,
                sender_is_practitioner=False,
                read_by_practitioner=False,
                read_by_patient=True
            )
            status = "Nachricht wurde gesendet!"
        else:
            status = "Bitte geben Sie eine Nachricht ein!"
    else:
        status = ""

    # mark incoming messages from practitioner as read by patient
    Message.objects.filter(
        patient=patient,
        practitioner=patient.practitioner,
        sender_is_practitioner=True,
        read_by_patient=False
    ).update(read_by_patient=True)

    messages = Message.objects.filter(
        patient=patient,
        practitioner=patient.practitioner
    ).order_by('-timestamp')

    return render(request, 'patient_messages.html', {
        'messages': messages,
        'status': status
    })

def view_patient_messages(request, patient_id):
    if not request.user.is_authenticated:
        return redirect('practitioner_login')
    try:
        practitioner = Practitioner.objects.get(user=request.user)
        patient = Patient.objects.get(id=patient_id, practitioner=practitioner)
    except (Practitioner.DoesNotExist, Patient.DoesNotExist):
        return redirect('practitioner_login')

    # handle practitioner sending a reply
    if request.method == 'POST':
        reply = request.POST.get('message')
        if reply:
            Message.objects.create(
                patient=patient,
                practitioner=practitioner,
                content=reply,
                sender_is_practitioner=True,
                read_by_practitioner=True,
                read_by_patient=False
            )
    # fetch messages
    messages = Message.objects.filter(
        patient=patient,
        practitioner=practitioner
    ).order_by('-timestamp')

    # Mark patient->practitioner messages as read_by_practitioner
    Message.objects.filter(
        patient=patient,
        practitioner=practitioner,
        sender_is_practitioner=False,
        read_by_practitioner=False
    ).update(read_by_practitioner=True)

    return render(request, 'practitioner_view_messages.html', {
        'patient': patient,
        'messages': messages
    })

def add_disease_for_patient(request, patient_id):
    practitioner = get_object_or_404(Practitioner, user=request.user)
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease = form.save(commit=False)
            disease.practitioner = practitioner
            disease.patient = patient
            disease.save()
            return redirect('practitioner_dashboard')
    else:
        form = DiseaseForm()

    return render(request, 'add_disease.html', {
        'form': form,
        'patient': patient
    })

def view_disease(request):
    patient = get_object_or_404(Patient, user=request.user)
    disease = Disease.objects.filter(patient=patient).order_by('-created_at').first()  # neuester Plan

    return render(request, 'view_disease.html', {
        'disease': disease
    })