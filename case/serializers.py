from rest_framework import serializers
from .models import RegItem, Item, Case, Quality, HistoryDrop, SiteConstructor, Category, UserProfile
from rest_framework.exceptions import APIException
from django.urls import reverse


class APIException202(APIException):
    status_code = 202


class RegItemSerializers(serializers.ModelSerializer):
    """ Сериализатор зарегистрированных предметов """
    quality = serializers.SlugRelatedField(slug_field="hexcolor", read_only=True)

    class Meta:
        model = RegItem
        exclude = ("id","price")


class ItemSerializers(serializers.ModelSerializer):
    """ Сериализатор выпавших предметов """
    item = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Item
        fields = "__all__"


class HistoryItemSerializers(serializers.ModelSerializer):
    """ Компонент предмет для сериализатора выпадения дропа """
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    item = RegItemSerializers()

    class Meta:
        model = Item
        exclude = ("id","price","is_active")


class HistoryDropSerializers(serializers.ModelSerializer):
    """ Сериализатор истории дропов """
    item = HistoryItemSerializers()
    case_photo = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = HistoryDrop
        fields = ('id','item','case_photo','profile_url')

    def get_case_photo(self, history):
        request = self.context.get('request')
        case_photo = history.case.photo.url
        return request.build_absolute_uri(case_photo)

    def get_profile_url(self, history):
        profile_url = history.item.user.profile.slug
        return profile_url


class DropItemSerializers(serializers.ModelSerializer):
    """ Сериализатор выпадения дропа """
    item = RegItemSerializers()
    sell_url = serializers.SerializerMethodField()
    case_slug = serializers.SerializerMethodField()

    class Meta:
        model = Item
        exclude = ("id","is_active","user")

    def get_case_slug(self, item):
        case_slug = item.history.first().case.slug
        return case_slug

    def get_sell_url(self, item):
        request = self.context.get('request')
        sell_slug = reverse('sell',args=(item.pk,))
        return request.build_absolute_uri(sell_slug)


class SellItemSerializers(serializers.ModelSerializer):
    """ Сериализатор продажи дропа """
    item = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Item
        fields = ("item","price")

    def validate(self, item, request):
        if not item.is_active:
            raise APIException202("Предмет уже продан.")
        elif item.user != request.user:
            raise APIException202("Вы не являетесь владельцем предмета.")
        return True


class CaseDetalSerializers(serializers.ModelSerializer):
    """ Сериализатор страницы с кейсом """
    drops = RegItemSerializers(many=True)
    possible_open = serializers.SerializerMethodField()

    class Meta:
        model = Case
        exclude = ("id","slug")

    def get_possible_open(self,case):
        request = self.context.get('request')
        balanse = request.user.profile.balanse
        price = case.price
        data={}
        if balanse-price>=0:
            data['possible'] = True 
        else:
            data['possible'] = False
            data['need'] = price-balanse
        return data


class CategoryCasesSerializers(serializers.ModelSerializer):
    """ Компонент кейсы для сериализатора категории """

    class Meta:
        model = Case
        exclude = ("drops","cases_open")


class CategorySerializers(serializers.ModelSerializer):
    """ Компонент категории для сериализатора конструктор сайта """
    cases = CategoryCasesSerializers(many=True)

    class Meta:
        model = Category
        exclude = ("description",)


class SiteConstructorSerializers(serializers.ModelSerializer):
    """ Сериализатор конструктора сайта """
    case_categories = CategorySerializers(many=True)

    class Meta:
        model = SiteConstructor
        fields = ("id","case_categories")


class ProfileSerializers(serializers.ModelSerializer):
    """ Сериализатор профиля """
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    inventory = ItemSerializers(many=True)

    class Meta:
        model = UserProfile
        exclude = ("id","slug")