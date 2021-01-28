from django.shortcuts import render
from django.http import HttpResponse
from .play import OpenCase
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import RegItem, Item, Case, Quality, HistoryDrop, SiteConstructor, Category, UserProfile
from .serializers import (
    HistoryDropSerializers,
    DropItemSerializers,
    SellItemSerializers,
    SiteConstructorSerializers,
    CaseDetalSerializers,
    ProfileSerializers,
)


class Profile(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializers
    lookup_field = "slug"


class SiteConstructor(ListAPIView):
    queryset = SiteConstructor.objects.filter(is_active=True)
    serializer_class = SiteConstructorSerializers


class LiveDrop(ListAPIView):
    queryset = HistoryDrop.objects.all().order_by("-id")[:20]
    serializer_class = HistoryDropSerializers


class DetailCase(RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseDetalSerializers
    lookup_field = "slug"
    permission_classes=[IsAuthenticated]


class DropItem(APIView):
    def get(self, request, slug):
        try:
            case = Case.objects.get(slug=slug)
        except Case.DoesNotExist:
            return Response(status=404)
        case = OpenCase(self.request,case)
        drop = case.get_drop()
        serializer = DropItemSerializers(drop, context={"request": request})
        return Response(serializer.data)


class SellItem(APIView):
    def get(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return Response(status=204)
        serializer = SellItemSerializers(item)
        if serializer.validate(item,request):
            item.is_active = False
            item.save()
            profile = item.user.profile
            profile.balanse += item.price
            profile.save()
            return Response(serializer.data)
        return Response(status=204)