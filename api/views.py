from django.shortcuts import render
import requests
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, NoteSerializer, UserSerializer2
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.models import AccessToken, Application
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from .models import Note, Users
from django.contrib.auth import logout
from oauth2_provider.models import RefreshToken


def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")


@permission_classes([AllowAny])
class CreateUser(APIView):
    serializer_class = UserSerializer2
    # permission_classes = [AllowAny]
    def post(self, request):
        sent_data = request.data
        print(f"the sent data is {sent_data}")
        data_request = self.serializer_class(data=request.data)
        if data_request.is_valid():
            print(f"the sent data is valid")
            username = data_request.data.get('username')
            password = data_request.data.get('password')
            confirm_password = data_request.data.get('confirm_password')
            print(f"the password {password} and confirm is {confirm_password}")
            if password == confirm_password and not User.objects.filter(username=username).exists():
                data_create = User.objects.create_user(username=username,password=password)
                data_create.save()
                print('--------------------- client id', settings.CLIENT_ID, '-------------------- client secret', settings.CLIENT_SECRET)
                app = Application.objects.get(client_id=settings.CLIENT_ID)
                print(f'application : {app.name}, client_id: {app.client_id}, client_secret: {app.client_secret}')
                sent_request = requests.post(settings.OAUTH_PROVIDER_URL + '/o/token/',
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    data={
                        'grant_type': 'password',
                        'username': username,
                        'password': password,
                        'client_id': settings.CLIENT_ID,
                        'client_secret': settings.CLIENT_SECRET,
                        'client_type': 'Public'
                    },
                )
                print("the data itself is ", sent_request.json())
                final = sent_request.json()
                user_created = UserSerializer(data_create).data
                final["user"] = user_created
                return Response(final, status=status.HTTP_201_CREATED)
            print("the sent data passwords do not match")
            return Response({"Message": "The passwords do not match "}, status=400)
        return Response({"Message": "An error occured now "}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        user_id = request.data.get('id')
        print(f"the user id is {user_id}")
        if user_id != None:
            user = Users.objects.get(id=user_id)
            print(f"the user is {user}")
            user_form = self.serializer_class(data=request.data) 
            if user != None and user_form.is_valid():
                user.username = user_form.data.get("username")
                user.password = user_form.data.get("password")
                user.confirm_password = user_form.data.get("confirm_password")
                user.save()
                return Response(UserSerializer2(user).data, status=200)
            return Response({"Message": "The user doesn't exist"}, status=404)
        return Response({"Message": "The user id doesn't exist"}, status=400)
    
    def get(self, request):
        queryset = Users.objects.all()
        print(f"users are {queryset}")
        return Response(UserSerializer2(queryset, many=True).data, status=200)

class LoginUserView(APIView):
    serializer_class = UserSerializer2
    def post(self, request):
        user = self.serializer_class(data=request.data)
        print("the user in question is ", user)
        print("username is ", request.data.get('username'))
        if user.is_valid():
            username = user.data.get("username")
            print('username is ', username)
            password = user.data.get("password")
            print('password is ', password)
            User_authenticated = authenticate(username=username, password=password)
            if User_authenticated:
                print('user is logged in')
                sent_request = requests.post(settings.OAUTH_PROVIDER_URL + '/o/token/',
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    data={
                        'grant_type': 'password',
                        'username': username,
                        'password': password,
                        'client_id': settings.CLIENT_ID,
                        'client_secret': settings.CLIENT_SECRET
                    },
                )
                print("the data itself is ", sent_request.json())
                final = sent_request.json()
                user_searched = User.objects.get(username=username)
                user_created = UserSerializer(user_searched).data
                final["user"] = user_created
                return Response(final, status=status.HTTP_201_CREATED)
            print("the credentials do not match")
            return Response({"Message": "The passwords do not match "}, status=status.HTTP_401_UNAUTHORIZED)
        print("iNCORRECCT STUFF")
        return Response({"Message": "The form is missing some values "}, status=status.HTTP_404_NOT_FOUND)

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        print("the serializer is ", serializer)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class NoteList(APIView):
    serializer_class = NoteSerializer

    def get(self, request, format=None):
        all_notes = Note.objects.all()
        return Response(NoteSerializer(all_notes, many=True).data, status=status.HTTP_200_OK)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class TokenRefreshView(APIView):

    def post(self, request):
        refresh_token_string = request.data.get("refresh_token")
        print("the refresh token is now ", refresh_token_string)
        if refresh_token_string is not None:
            print("entered ref ")
            r = requests.post(
                settings.OAUTH_PROVIDER_URL + '/o/token/',
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token_string,
                    'client_id': settings.CLIENT_ID,
                    'client_secret': settings.CLIENT_SECRET
                },
            )
            final = r.json()
            print("final value is ", final)
            return Response(final, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     refresh_token = RefreshToken.get(token=refresh_token_string)
        #     access_token = refresh_token.access_token
        #     return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)
        # except RefreshToken.DoesNotExist:
        #     return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def remok_token(request):
    access_token_string = request.data.get("access_token")
    print("the refresh token is now ", access_token_string)
    if access_token_string is not None:
        r = requests.post(
            settings.OAUTH_PROVIDER_URL + '/o/revoke_token/',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'token': access_token_string,
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET
            },
        )