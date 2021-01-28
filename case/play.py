import random
import numpy
from .models import *


class OpenCase():
    def __init__(self,request,case):
        self.user = request.user
        self.profile = self.get_profile()
        self.case = case

    def get_profile(self):
        profile = UserProfile.objects.get(user__username=self.user)
        return profile

    def formation_chanse(self):
        items = self.case.drops.all()
        tickets = 0
        new_tickets = 0
        chanse = {}
        for item in items:
            new_tickets = tickets + item.quality.chance
            item_chanse = numpy.arange(tickets,new_tickets,0.01)
            chanse[item.name] = [round(num,2) for num in item_chanse]
            tickets = new_tickets
        return tickets,chanse

    def case_open(self,tickets,chanse):
        rand_ticket = random.uniform(0, tickets)
        rand_ticket = round(rand_ticket,2)
        for name,ranges in chanse.items():
            if rand_ticket in ranges:
                item = RegItem.objects.get(name=name)
                drop = Item.objects.create(user=self.user,item=item,price=item.price)
                return drop

    def save_info(self,drop):
        self.profile.balanse -= self.case.price
        self.profile.inventory.add(drop)
        self.profile.cases_open += 1
        self.profile.save()
        self.case.cases_open+=1
        self.case.save()
        history = HistoryDrop.objects.create(case=self.case,item=drop)
        history.save()
                
    def get_drop(self):
        tickets,chanse = self.formation_chanse()
        drop = self.case_open(tickets,chanse)
        self.save_info(drop)
        return drop