from rest_framework.response import Response
import jwt, json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import status, exceptions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
import sys

[sys.path.append(i) for i in ['.', '..']]
from database.models import *
from database.DBApi import db_connection

from database.login import *


class JAuthentificated(BasePermission):

    def has_permission(self, request, view):
        return type(request.user) != AnonymousUser


class LoginView(APIView):

    def post(self, request):
        if not request.data:
            return Response(json.dumps({'Error': "Please provide username/password"}), status=401)

        username = request.data['username']
        password = request.data['password']
        user = login(email=username, password=password, con=db_connection)
        if user:
            payload = {
                'id': user.id
            }

            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY").decode("utf-8")}
            print('success')
            return Response(
                jwt_token,
                status=200,
                content_type="application/json"
            )
        else:
            return Response(
                {'Error': "Invalid crefdentials"},
                status=401,
                content_type="application/json"
            )


class TokenAuthentication(BaseAuthentication):
    model = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None
        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, "SECRET_KEY")
            userid = payload['id']
            user = User.get_user_with_correct_type(userid, db_connection)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid token")
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid token")

        return user, token

    def authenticate_header(self, request):
        return 'Token'


class RegView(APIView):

    def post(self, request):
        try:
            name = request.data['username']
            password = request.data['password']
            age = 12  # request.data['age']
            sex = request.data['sex']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            # nid = request.data['nid']
            address = request.data['address']
        except:
            return Response(status=400, data={'Error': 'Not all fields provided'}, content_type='application/json')
        user = registration(username=name,
                            password=password,
                            age=age,
                            sex=sex,
                            first_name=first_name,
                            last_name=last_name,
                            address=address,
                            con=db_connection)
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'Error': 'User with given username already exists'})
        else:
            return Response(status=status.HTTP_200_OK, data={'Message': 'Successfully registered'})


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [JAuthentificated]

    def get(self, request):
        user = request.user
        return Response(status=status.HTTP_200_OK,
                        data={'username': user.id,
                              'age': int(user.age),
                              'sex': user.sex,
                              'address': user.address,
                              'first_name': user.first_name,
                              'last_name': user.last_name})


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [JAuthentificated]

    def post(self, request):
        old_pass = request.data['old_password']
        if request.user.password != old_pass:
            return Response(status=403, data={'Error': 'Old password is not correct'})
        else:
            new_pass = request.data['new_password']
            request.user.password = new_pass
            return Response(status=200, data='Password successfully changed')
