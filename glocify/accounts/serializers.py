# restframework imports
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import exceptions

# djnago imports
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
#utils
from utils import res_codes

# in house apps import
from .models import User, Contact

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    first_name = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    last_name = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(
        min_length=8,
        style={
            'input_type': 'password', 
        }
    )

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True, },
        }

    def create(self, validated_data):
        user_obj = User.objects.create(**validated_data)
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        return user_obj

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        style={
            'input_type': 'password', 
        }
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivate"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide email and password both"
            raise exceptions.ValidationError(msg)
        return data


class ContactMeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    Name = serializers.CharField(
        required=True,
    )

    class Meta:
        model = Contact
        fields = [
            'id',
            'email',
            'Name'
        ]
    def create(self, validated_data):
        contact_obj = Contact.objects.create(**validated_data)
        
        contact_obj.save()
        return contact_obj
