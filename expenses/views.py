from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from .serializers import ExpenseSerializer
from.models import Expense
from .permissions import  IsOwner
from .paginations import ExpensePagination


class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = ExpensePagination

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        return instance

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)