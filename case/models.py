from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .service import resize_photo, slugify


class Quality(models.Model):
    name = models.CharField("Название качества",max_length=100)
    hexcolor = models.CharField("Цвет качества",max_length=7, default="#ffffff")
    chance = models.FloatField("Шанс выпадения",max_length=100) 

    def __str__(self):
        return f"{self.name}"


class RegItem(models.Model):
    name = models.CharField("Название предмета",max_length=100,unique=True)
    photo = models.ImageField("Фото предмета",upload_to="items", default="items/no_products_found.png",blank=True)
    quality = models.ForeignKey(Quality,verbose_name="Качество предмета",on_delete=models.CASCADE)
    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwards):
        super().save(*args, **kwards)
        image = resize_photo(self.photo.path)


class Item(models.Model):
    item = models.ForeignKey(RegItem,verbose_name="Предмет",on_delete=models.CASCADE)
    price = models.FloatField("Цена дропа", default=0)
    user = models.ForeignKey(User,verbose_name="Пользователь",on_delete=models.CASCADE)
    is_active = models.BooleanField("Предмет не продан",default=True)

    def __str__(self):
        return f"{self.item.name}"


class Case(models.Model):
    name = models.CharField("Название",max_length=100,unique=True)
    photo = models.ImageField("Фото кейса",upload_to="case", default="case/clutch-case.png",blank=True)
    drops = models.ManyToManyField(RegItem,verbose_name="Дроп", related_name="drops")
    slug = models.SlugField("Ссылка на кейс",blank=True)
    price = models.IntegerField("Цена")
    cases_open = models.IntegerField("Кейсов открыто",default=0)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("case", kwargs={"slug": self.slug})

    def save(self, *args, **kwards):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwards)
        image = resize_photo(self.photo.path)


class HistoryDrop(models.Model):
    case = models.ForeignKey(Case,verbose_name="Название кейса",on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Item,verbose_name="Выпал предмет",on_delete=models.CASCADE,related_name="history")

    def __str__(self):
        return f"{self.item}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь",on_delete=models.CASCADE,related_name="profile")
    slug = models.SlugField("Ссылка на профиль", blank=True)
    inventory = models.ManyToManyField(Item,verbose_name="Предметы",blank=True)
    cases_open = models.IntegerField("Кейсов открыто",default=0)
    balanse = models.FloatField("Баланс",default=200)

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwards):
        if not self.slug:
            self.slug = self.user
        return super().save(*args, **kwards)


    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


class Category(models.Model):
    name = models.CharField("Название категории",max_length=20)
    cases = models.ManyToManyField(Case,verbose_name="Кейсы категории")
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.name}"


class SiteConstructor(models.Model):
    name = models.CharField("Название категории",max_length=100)
    is_active = models.BooleanField("Используется", default=False)
    case_categories = models.ManyToManyField(Category, verbose_name="Категории кейсов")
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwards):
        if self.is_active:
            self.deactive_constructors()
        super().save(*args, **kwards)

    def deactive_constructors(self):
        constructors = SiteConstructor.objects.filter(is_active=True)
        for item in constructors:
            item.is_active = False
            item.save()