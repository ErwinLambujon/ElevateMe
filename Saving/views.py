from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .models import TwoVennDiagram, TwoProblemStatement, ThreeProblemStatement, ThreeVennDiagram


class SaveProblemStatement(View):

    @method_decorator(login_required(login_url="authenticate:login"))
    def get(self, request):
        pass

    def post(self, request):

        venn_diagram = request.session.get('venn_scopes')
        checked_checkboxes = request.POST.getlist('checkbox_group')

        session_checked = request.session.get('checked_checkboxes')

        lists_checked_checkboxes = []
        if session_checked:

            lists_checked_checkboxes.extend(session_checked)
            lists_checked_checkboxes.extend(checked_checkboxes)

            request.session['checked_checkboxes'] = lists_checked_checkboxes
        else:
            request.session['checked_checkboxes'] = checked_checkboxes

        print(request.session.get('checked_checkboxes'))
        auth = request.session.get('auth')
        user = User.objects.get(username=auth["username"])

        if request.method == "POST":
            field1 = venn_diagram['field1']
            field2 = venn_diagram['field2']
            field3 = venn_diagram['field3']
            filter_field = venn_diagram['filter']

            setting = venn_diagram['settings']
            if setting == "2":
                existing_venn = TwoVennDiagram.objects.filter(field1=field1, field2=field2, field3=field3, filter=filter_field,
                                                              user_fk=user).first()

                if not existing_venn:
                    two_venn = TwoVennDiagram(field1=field1, field2=field2, field3=field3,filter=filter_field, user_fk=user)
                    two_venn.save()
                else:
                    two_venn = existing_venn

                # Do something with the checked checkboxes
                for checkbox_value in checked_checkboxes:
                    problem_statement = TwoProblemStatement(statement=checkbox_value, user_fk=user, venn_fk=two_venn)
                    problem_statement.save()

            elif setting == "3":
                existing_venn = ThreeVennDiagram.objects.filter(field1=field1, field2=field2, field3=field3,filter=filter_field,
                                                                user_fk=user).first()

                if not existing_venn:
                    three_ven = ThreeVennDiagram(field1=field1, field2=field2, field3=field3, filter=filter_field, user_fk=user)
                    three_ven.save()

                else:
                    three_ven = existing_venn

                for checkbox_value in checked_checkboxes:
                    problem_statement = ThreeProblemStatement(statement=checkbox_value, user_fk=user, venn_fk=three_ven)
                    problem_statement.save()
        return redirect('homepage:home')


class Save(View):
    @method_decorator(login_required(login_url="authenticate:login"))
    def get(self, request):
        auth = request.session.get('auth')
        user = User.objects.get(username=auth["username"])

        twoPS = TwoProblemStatement.objects.filter(user_fk=user)
        threePS = ThreeProblemStatement.objects.filter(user_fk=user)

        context = {
            'twoPS_data': twoPS,
            'threePS_data': threePS
        }

        return render(request, 'save.html', context)

    def post(self, request):
        auth = request.session.get('auth')
        user = User.objects.get(username=auth["username"])

        twoPS = TwoProblemStatement.objects.filter(user_fk=user)
        threePS = ThreeProblemStatement.objects.filter(user_fk=user)

        context = {
            'twoPS_data': twoPS,
            'threePS_data': threePS
        }

        return render(request, 'save.html', context)


class SaveOperation(View):
    @method_decorator(login_required(login_url="authenticate:login"))
    def get(self, request, operation):
        pass

    def post(self, request, operation):
        auth = request.session.get('auth')

        if request.method == "POST":
            button_value = request.POST.get('button')

            statement = request.POST.get('radiobutton_group')

            pk = int(operation)

            if button_value == "button2.1":

                # PERFORM SAVE
                twoPS = TwoProblemStatement.objects.get(id=pk)
                old_statement = twoPS.statement
                twoPS.statement = statement
                twoPS.save()

                session_checked = request.session.get('checked_checkboxes')

                if session_checked:
                    print(old_statement in session_checked)
                    if old_statement in session_checked:
                        if statement not in session_checked:
                            new_session = [item for item in session_checked if item != old_statement]
                            request.session['checked_checkboxes'] = new_session
                            print(new_session)
                        else:
                            print(session_checked)
                            request.session['checked_checkboxes'] = session_checked

            elif button_value == "button2.2":

                twoPS = TwoProblemStatement.objects.get(id=pk)
                statement = twoPS.statement
                twoPS.delete()

                session_checked = request.session.get('checked_checkboxes')

                if session_checked:
                    if statement in session_checked:
                        session_checked.remove(statement)

                request.session['checked_checkboxes'] = session_checked

            elif button_value == "button3.1":
                threePS = ThreeProblemStatement.objects.get(id=pk)
                old_statement = threePS.statement
                threePS.statement = statement
                threePS.save()

                session_checked = request.session.get('checked_checkboxes')

                a = 5
                b = 10
                print(f"{a+b=}")

                if session_checked:
                    print(old_statement in session_checked)
                    if old_statement in session_checked:
                        print("NI SUD ANG OLD STATEMENT")
                        if statement not in session_checked:
                            print("NI SUD ANG NEW STATEMENT")
                            new_session = [item for item in session_checked if item != old_statement]
                            request.session['checked_checkboxes'] = new_session
                        else:
                            request.session['checked_checkboxes'] = session_checked
            elif button_value == "button3.2":
                threePS = ThreeProblemStatement.objects.get(id=pk)
                statement = threePS.statement
                threePS.delete()

                session_checked = request.session.get('checked_checkboxes')

                if session_checked:
                    if statement in session_checked:
                        session_checked.remove(statement)

                request.session['checked_checkboxes'] = session_checked
        return redirect('Saving:savePage')


def TwoPopUpVenn(request, instance_id):
    pk = int(instance_id)
    twoPS = TwoProblemStatement.objects.get(id=pk)
    venn = twoPS.venn_fk
    data = {
        'field1': venn.field1,
        'field2': venn.field2,
        'filter': venn.filter
    }
    return JsonResponse(data)

def ThreePopUpVenn(request, instance_id):
    pk = int(instance_id)
    threePS = ThreeProblemStatement.objects.get(id=pk)
    venn = threePS.venn_fk
    data ={
        'field1': venn.field1,
        'field2': venn.field2,
        'field3': venn.field3,
        'filter': venn.filter
    }
    return JsonResponse(data)