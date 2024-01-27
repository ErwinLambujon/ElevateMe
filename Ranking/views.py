from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from Saving.models import TwoProblemStatement, ThreeProblemStatement


# This method is only use for redirecting to that page
def ranking(request):
    context = request.session.get('selected_checkboxes_table')

    store = request.session.get('ranked_problem')

    print(store)

    return render(request, "Ranking.html", {
        "context": context,
        "ranking_setting": request.session.get('ranking_setting'),
        "valid": request.session.get('valid'),
        "root_problem": request.session.get('ranked_problem')
    })


class ShowLists(View):
    @method_decorator(login_required(login_url="authenticate:login"))
    def get(self, request, setting):
        pass

    def post(self, request, setting):
        global data
        if request.method == "POST":
            request.session['ranking_setting'] = setting

            if setting == 2:
                auth = request.session.get('auth')
                user = User.objects.get(username=auth["username"])

                twoPS = TwoProblemStatement.objects.filter(user_fk=user)

                data = [
                    {
                        'id': ps.id,
                        'statement': ps.statement,
                        'user_fk': ps.user_fk.id,
                        'venn_fk': ps.venn_fk.id if ps.venn_fk else None,
                    }
                    for ps in twoPS
                ]
                data = {'data': data}
                return JsonResponse(data)
            elif setting == 3:
                auth = request.session.get('auth')
                user = User.objects.get(username=auth["username"])

                threePS = ThreeProblemStatement.objects.filter(user_fk=user)
                data = [
                    {
                        'id': ps.id,
                        'statement': ps.statement,
                        'user_fk': ps.user_fk.id,
                        'venn_fk': ps.venn_fk.id if ps.venn_fk else None,
                    }
                    for ps in threePS
                ]

                data = {'data': data}
                return JsonResponse(data)

        return HttpResponse("FAILED")


class AddToTable(View):
    def get(self, request):
        pass;

    def post(self, request):
        if request.method == "POST":
            selected_checkboxes = request.POST.getlist('checkbox_group')

            auth = request.session.get('auth')
            user = User.objects.get(username=auth["username"])

            PS_list = []

            setting = request.session.get('ranking_setting')

            if setting == 2:
                for checkbox_value in selected_checkboxes:
                    twoPS_instance = TwoProblemStatement.objects.filter(user_fk=user, statement=checkbox_value)
                    PS_list.append(twoPS_instance)
            else:
                for checkbox_value in selected_checkboxes:
                    three_PS = ThreeProblemStatement.objects.filter(user_fk=user, statement=checkbox_value)
                    PS_list.append(three_PS)

            new_context = {
                'items': [
                    {'id': item.id, 'statement': item.statement}
                    for queryset in PS_list
                    for item in queryset
                ]
            }

            request.session['selected_checkboxes_table'] = new_context
            request.session['valid'] = True if len(selected_checkboxes) > 2 else False

            return redirect('Ranking:ranking')
        return HttpResponse("No")
