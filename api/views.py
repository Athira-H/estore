from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import serializers
# from rest_framework.views import APIView



from api.models import Products,Carts,Reviews
from api.serializers import ProductSerializer,CartSerializer,ReviewSerializer

from rest_framework.decorators import action




# Create your views here.
class ProductView(ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Products.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    # authentication_classes=[authentication.TokenAuthentication]

    
    @action(methods=["GET"],detail=False)
    def categories(self,request,*args,**kw):
        qs=Products.objects.values_list("category",flat=True).distinct()
        return Response(data=qs)

    def list(self, request, *args, **kwargs):
        qs=Products.objects.all()
        if "category" in request.query_params:
            qs=qs.filter(category=request.query_params.get("category"))
        serializer=ProductSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["POST"],detail=True)
    def addto_cart(self,request,*args,**kw):

        product=self.get_object()
        user=request.user
        serializer=CartSerializer(data=request.data,context={"user":user,"product":product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kw):

        product=self.get_object()
        user=request.user
        serializer=ReviewSerializer(data=request.data,context={"user":user,"product":product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


            
class CartsView(ViewSet):
    permission_classes=[permissions.IsAuthenticated]
    # authentication_classes=[authentication.TokenAuthentication]
    def list(self,request,*args,**kw):
        qs=Carts.objects.filter(user=request.user)
        serializer=CartSerializer(qs,many=True)
        return Response(data=serializer.data)

    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        object=Carts.objects.get(id=id)
        if object.user==request.user:
            object.delete()
            return Response(data="deleted")
        else:
            raise serializers.ValidationError("you have no permission to perform this operation")


from rest_framework import mixins
from rest_framework import generics
from api.models import Reviews

class ReviewDeleteView(mixins.DestroyModelMixin,generics.GenericAPIView):

    serializer_class=ReviewSerializer
    queryset=Reviews.objects.all()
    def delete(self,request,*args,**kw):
        id=kw.get("pk")
        review=Reviews.objects.get(id=id)
        if review.user==request.user:
            return self.destroy(request,*args,**kw)
        else:
            raise serializers.ValidationError("you have no permission")
        