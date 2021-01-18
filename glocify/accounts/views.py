from django.shortcuts import render

# restframework imports
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

#djnago imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login, logout as django_logout
from django.utils import timezone

from .serializers import (
	UserCreateSerializer, 
	UserLoginSerializer,
	ContactMeSerializer
)

from utils import res_codes
from django.core.mail import send_mail

User = get_user_model()


class SignUpView(APIView):
	serializer_class = UserCreateSerializer

	def post(self, request, *args, **kwargs):

		"""
		### Body:
		```
		{
		    "first_name": "v",
		    "last_name": "s",
		    "email": "vs@yopmail.com",
		    "password": "password",

		}
		```

		#### Response (success):
		```
		{
		    "code": 1001,
		    "msg": "Account created successfully",
		    "data": {
		        "id": "db54e0a6-a9e3-40b6-b2d0-1a54b3583320",
		        "first_name": "v",
		        "last_name": "s",
		        "email": "vs@yopmail.com",
		        "profile": {
		            "country": "India",
		            "date_of_birth": "2019-02-19",
		            "organization": "School"
		        }
		    }
		}
		```

		#### Response (error):
		```
		{
		    "code": 1000,
		    "msg": "Invalid post data provided",
		    "data": {
		        "first_name": [
		            "This field may not be blank."
		        ],
		        "password": [
		            "This field may not be blank."
		        ],
		        "email": [
		            "This field may not be blank."
		        ],
		        "last_name": [
		            "This field may not be blank."
		        ],
		        "profile": {
		            "date_of_birth": [
		                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
		            ],
		            "organization": [
		                "This field may not be blank."
		            ],
		            "country": [
		                "This field may not be blank."
		            ]
		        }
		    }
		}
		```

		#### Response (error):
		```
		{
			"code": 1000,
			"msg": "Invalid post data provided",
			"data": {
				"email": [
					"This field must be unique."
				]
			}
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "msg": "Invalid post data provided",
		    "data": {
		        "profile": {
		            "date_of_birth": [
		                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
		            ]
		        }
		    }
		}
		```
		"""
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			user_obj = serializer.save()

			return Response(
				res_codes.get_response_dict(
					res_codes.SIGNUP_SUCCESS,
					serializer.data,
				),
				status=status.HTTP_201_CREATED,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.INVALID_POST_DATA,
				serializer.errors,
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class LoginView(APIView):
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]
		django_login(request, user)
		token, create = Token.objects.get_or_create(user=user)
		return Response(
			{
				"token": token.key,
				"User": user.get_full_name()
			},
			status=200
		)


class LogOutView(APIView):
	authentication_classes = (TokenAuthentication, )

	def get(self, request, format=None):
		django_logout(request)
		return Response(
			status=204
		)


class ContactMe(APIView):
	serializer_class = ContactMeSerializer

	def post(self, request, *args, **kwargs):
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		superusers_emails = User.objects.filter(is_superuser=True).first().email
		if serializer.is_valid():
			subject = 'GLOCIFY'
			msg = 'request from email: {}'.format(data.get('email'))
			send_mail(
			    subject,
			    msg,
			    'anaconda.wb@gmail.com',
			    [superusers_emails],
			)
			serializer.save()
		return Response(
			{
				"message": "Please contact the admin"
			},
			status=200
		)

