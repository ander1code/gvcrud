from django.db.models import Max, Min, Avg, Count, Sum, Q

class Reports:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Reports, cls).__new__(cls)
        return cls.__instance

    def __init__(self, objects):
        self.objects = objects or objects.none()
        self.max_income = self.objects.aggregate(Max('income_range'))['income_range__max']
        self.min_income = self.objects.aggregate(Min('income_range'))['income_range__min']
        self.avg_income = self.objects.aggregate(Avg('income_range'))['income_range__avg']

    def get_highest_income_person(self):
        return self.objects.filter(income_range=self.max_income).first()

    def get_lowest_income_person(self):
        return self.objects.filter(income_range=self.min_income).first()

    def get_people_above_average_income(self):
        return self.objects.filter(income_range__gt=self.avg_income)

    def get_people_below_average_income(self):
        return self.objects.filter(income_range__lt=self.avg_income)

    def get_people_with_average_income(self):
        return self.objects.filter(income_range=self.avg_income)

    def count_by_gender(self, gender):
        return self.objects.aggregate(
            total=Count('id', filter=Q(gender__exact=gender))
        )['total'] or 0

    def total_income_sum(self):
        return self.objects.aggregate(
            total=Sum('income_range')
        )['total'] or 0
