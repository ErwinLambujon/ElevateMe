from django.contrib import admin

from .models import TwoProblemStatement, ThreeProblemStatement, TwoVennDiagram, ThreeVennDiagram

# Register your models here.
admin.site.register(TwoProblemStatement)
admin.site.register(ThreeProblemStatement)
admin.site.register(TwoVennDiagram)
admin.site.register(ThreeVennDiagram)