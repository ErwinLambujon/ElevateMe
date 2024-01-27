import openai
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from Saving.models import TwoProblemStatement, ThreeProblemStatement


# Create your views here.
def FiveWhys(request):
    root_problem = request.session.get('ranked_problem')
    pk = request.session.get('pk_rankedPS')
    setting = request.session.get('ranking_setting')

    return render(request, "Whys.html",
                  {
                      "rankedPS": root_problem,
                      "pk": pk,
                      "setting": setting
                  })


class RootProblemStatement(View):
    def get(self, request):
        pass

    def post(self,request, pk):
        if request.method == "POST":

            request.session['pk_rankedPS'] = pk

            root_problem = request.POST.get('radiobutton_group')

            rp = request.session.get('root_problem')
            if rp:
                del request.session['root_problem']
            fw = request.session.get('fiveWhys')
            if fw:
                del request.session['fiveWhys']
            ranked_prob = request.session.get('ranked_problem')

            if ranked_prob:
                del request.session['ranked_problem']

            request.session['ranked_problem'] = root_problem

            return redirect('Whys:5-whys')



def GenerateFiveWhys(request, value):
    if request.method == "POST":
        generated_five_whys = openAiFiveWhy(value)

        data = [
            {
                'statement': ps
            }
            for ps in generated_five_whys.values()
        ]

        request.session['fiveWhys'] = data

        print(data)

        return JsonResponse({
            "fiveWhys": data
        })


    return HttpResponse("POST")

def openAiFiveWhy(value):
    openai.api_key = "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"

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{
        "role": "user",
        "content": f"Subject the {value} to a 5-Why analysis. "
                   f"Generate five whys to uncover the underlying issue behind {value}. Make it relevant to the {value} and understandable."
                   f"Please dont include any explanation just generate all the whys statement."

    }])

    response_list = completion.choices[0].message.content.split('\n')

    print(response_list)

    questions_dict = {}

    for i, question in enumerate(response_list, start=1):
        # Split each question and take the second part (after the dot)
        question_without_number = question.split('. ', 1)[1].strip()
        questions_dict[i] = question_without_number

    return questions_dict


def showTwoHistory(request, pk):
    ranking_setting = request.session.get('ranking_setting')
    new_pk = int(pk)
    twoPS = TwoProblemStatement.objects.get(id=pk)
    venn = twoPS.venn_fk
    data = {
        'field1': venn.field1,
        'field2': venn.field2,
        'filter': venn.filter
    }

    print(type(new_pk))

    return JsonResponse(
        {
            'data': data,
            'setting': ranking_setting
        }
    )


def showThreeHistory(request, pk):
    ranking_setting = request.session.get('ranking_setting')
    new_pk = int(pk)
    threePS = ThreeProblemStatement.objects.get(id=pk)
    venn = threePS.venn_fk

    data = {
        'field1': venn.field1,
        'field2': venn.field2,
        'field3': venn.field3,
        'filter': venn.filter

    }

    return JsonResponse(
        {
            'data': data,
            'setting': ranking_setting
        }
    )