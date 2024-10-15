from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
import requests
from django.contrib.auth.models import User
from .models import Books
from rest_framework import generics, status
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from oauth2_provider.models import AccessToken

# Create your views here.
# @permission_classes([AllowAny])
class CreateBooks(APIView):
    permission_classes = [AllowAny]
    serializer_class = BookSerializer
    def post(self, request):
        data_send = self.serializer_class(data=request.data)
        print("the data I am sending is ", request.data)
        token = request.data.get("token")
        print("Token is sent equals --------------------------------------", token)
        token_obj = get_object_or_404(AccessToken, token=token)
        if not token_obj.is_valid() and token_obj.is_expired():
            print("Token is not valid 000000000000000000000000")
            token_obj.revoke()
            return Response({'Message': f"The token '{token_obj}' was revoked successfully", 'status': True}, status=401)
        name = request.data.get("name")
        resume = request.data.get("resume")
        user_id = request.data.get("user_id")
        if "name" and "resume" and "user_id" in request.data:
            print("Serializer is valid ")
            all_users = User.objects.get(id=user_id)
            print("User is found ", all_users)
            if all_users != None:
                user = all_users
                print("User exists", user)
                created_book = Books.objects.create(name=name, resume=resume)
                created_book.user.add(user)
                created_book.save()
                print("Book created successsfully!! ", created_book)
                return Response(BookSerializer(created_book).data, status=status.HTTP_201_CREATED)
            print("User not found please try again!!!")
            return Response({"Message": "The user don't exist please try again man "}, status=status.HTTP_404_NOT_FOUND)
        print("The form is not containing all the fields!!!")
        return Response({"Message": "Not all the fields are valid "}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
@permission_classes([AllowAny])
def get_user_books(request):
    serializer_class = BookSerializer
    data_send = serializer_class(data=request.data)
    print("the data I am sending is ", request.data)
    token = request.data.get("token")
    print("Token is sent equals --------------------------------------", token)
    token_obj = get_object_or_404(AccessToken, token=token)
    if not token_obj.is_valid() and token_obj.is_expired():
        print("Token is not valid 000000000000000000000000")
        token_obj.revoke()
        return Response({'Message': f"The token '{token_obj}' was revoked successfully", 'status': True}, status=401)
    users_id = request.data.get("user_id")
    if users_id != None:
        print("User not none")
        users = User.objects.get(id=users_id)
        print("Got user is ", users)
        if users != None:
            # queryset = Books.objects.filter(user=users)
            # print("All the books are ",  queryset)
            # user_books = users.user_books.all()
            user_books = users.user_books.get()
            print("All the user books are ", user_books)
            return Response(BookSerializer(user_books, many=True).data, status=201)
        print("The form is not containing all the fields!!!")
        return Response({"Message": "The user don't exist please try again man "}, status=status.HTTP_404_NOT_FOUND)
    return Response({"Message": "Not all the fields are valid "}, status=status.HTTP_403_FORBIDDEN)