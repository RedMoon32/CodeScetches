from rest_framework.response import Response
import jwt, json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import status, exceptions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from database.models import *
from database.DBApi import db_connection
from Clinic.Profile_Views import TokenAuthentication, JAuthentificated
from database.login import *


class ApointmentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [JAuthentificated]

    def post(self, request):

        type_of_user = User.get_type_by_id(request.user.id, db_connection)
        try:
            time = int(request.data['time'])
            if time < 0 or time > 10:
                raise ValueError
            day = request.data['date']
        except:
            return Response(status=400)

        doc_id = None
        pat_id = None

        if type_of_user is 'doctor':
            if 'doctor' in request.data and request.data['doctor'] != request.user.id:
                return Response(status=400,
                                data={'Error': 'Doctor can not create appointments for other doctors'})
            doc_id = request.user.id
            pat_id = request.data['patient']

        elif type_of_user is 'patient':
            if 'patient' in request.data and request.data['patient'] != request.user.id:
                return Response(status=400,
                                data={'Error': 'Patient can not create appointments for other patients'})
            pat_id = request.user.id
            doc_id = request.data['doctor']

        elif type_of_user is 'receptionist':
            pat_id = request.data['patient']
            doc_id = request.data['doctor']
        else:
            return Response(status=400, data={'Error': 'No access'})

        doctor = Doctor.get_by_id(doc_id, db_connection)
        if doctor is None or len([app for app in doctor.get_appointments(db_connection) if
                                  app.date == day and app.time == time]) > 0:
            return Response(status=400, data={'Error': 'Doctor not available'})

        patient = Patient.get_by_id(pat_id, db_connection)
        if patient is None or len([app for app in patient.get_records(db_connection) if
                                   app.date == day and app.time == time]) > 0:
            return Response(status=400, data={'Error': 'Patient not available'})
        app = Appointment(date=day, time=time, patient=patient, doctor=doctor)

        if app.save(db_connection) is None:
            return Response(status=400, data={'Error': 'Can not create appointment on this slot'})
        else:
            return Response(status=200, data='Appointment created')

    def get(self, request):
        appointments = []
        type_of_user = request.user.type
        if type_of_user == "doctor":
            appointments = request.user.get_appointments(db_connection)
        elif type_of_user == "patient":
            appointments = request.user.get_records(db_connection)
        elif type_of_user == "receptionist":
            appointments = Appointment.get_all(db_connection)
        else:
            return Response(status=400, data={'Error': 'No access'})
        return Response(status=200, data=[
            {'doctor': app.doctor.id,
             'patient': app.patient.id, 'time': app.time, 'date': app.date} for
            app in
            appointments])


class DoctorsView(APIView):

    def get(self, request):
        doctors = Doctor.get_all(db_connection)
        return Response(status=200, data=[
            {'Doctor': doctor.id, 'room': 1, 'type': 'Kek', 'name': doctor.first_name + " " + doctor.last_name} for
            doctor in doctors])
