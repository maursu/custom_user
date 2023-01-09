from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()

class Registrationserializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password= serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def valudate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        return email

    def validate(self, attr):
        password = attr.get('password')
        password2 = attr.pop('password_confirm')
        if password != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attr

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такой пользователь не найден =('
            )
        return email
    
    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(
                username = email,
                password=password,
                request=request,
            )
            if not user:
                raise serializers.ValidationError(
                    'Не верный емаил или пароль'
                )
        else:
            raise serializers.ValidationError(
                'Емаил и пароль не должжны быть пустыми'
            )
        data['user'] = user
        return data