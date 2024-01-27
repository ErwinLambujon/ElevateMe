import openai
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views import View
from django.shortcuts import render, redirect

class VennDiagramFilter(View):
    template_name = "homepage.html"

    @method_decorator(login_required(login_url="authenticate:login"))
    def get(self, request, venn_settings):
        venn_diagram = request.session.get('venn_scopes')
        generate_response = request.session.get('openai')
            
        context = {
            "venn_scopes": venn_diagram,
            "generate_response": generate_response
        }

        return render(request, self.template_name, context)

    def post(self, request, venn_settings):
        if request.method == "POST":
            if venn_settings == "2":
                field1 = request.POST.get("field1")
                field2 = request.POST.get("field2")
                field3 = ""
                field4 = request.POST.get("filter")

                venn_scopes = {
                    'settings': venn_settings,
                    'field1': field1,
                    'field2': field2,
                    'field3': field3,
                    'filter': field4,
                }

                request.session['venn_scopes'] = venn_scopes

                generate_response = request.session.get('openai')
                checked_checkboxes = request.session.get('checked_checkboxes')


                context = {
                    "venn_scopes": venn_scopes,
                    "generate_response": generate_response,
                    "checked": checked_checkboxes
                }

            elif venn_settings == "3":
                field1 = request.POST.get("field1")
                field2 = request.POST.get("field2")
                field3 = request.POST.get("field3")
                field4 = request.POST.get("filter")

                venn_scopes = {
                    'settings': venn_settings,
                    'field1': field1,
                    'field2': field2,
                    'field3': field3,
                    'filter': field4,
                }

                generate_response = request.session.get('openai')

                request.session['venn_scopes'] = venn_scopes

                checked_checkboxes = request.session.get('checked_checkboxes')

                context = {
                    "venn_scopes": venn_scopes,
                    "generate_response": generate_response,
                    "checked": checked_checkboxes
                }
                

        return redirect("homepage:home")


class GeneratePS(View):
    @method_decorator(login_required(login_url="authenticate:login"))
    def get(self, request):
        return render(request, "homepage.html")

    def post(self, request):
        if request.method == "POST":
            venn_diagram = request.session.get('venn_scopes')

            checked_checkboxes = request.session.get('checked_checkboxes')

            try:
                setting = venn_diagram["settings"]
            except Exception as e:
                return redirect('homepage:errorPage')

            # 2 VENN DIAGRAM SETTING
            if setting == "2":
                field1 = venn_diagram['field1']
                field2 = venn_diagram['field2']
                field3 = ""
                field4 = venn_diagram['filter']

                try:
                    generate_response = generateAi(field1, field2, field3, field4)

                    if checked_checkboxes:
                        del request.session['checked_checkboxes']
                except Exception as e:
                    print(e)
                    return redirect('homepage:errorPage')   

                # Perform any additional processing with the data if needed
                request.session['openai'] = generate_response

            # 3 VENN DIAGRAM SETTING
            elif setting == "3":

                field1 = venn_diagram['field1']
                field2 = venn_diagram['field2']
                field3 = venn_diagram['field3']
                field4 = venn_diagram['filter']

                # Perform any additional processing with the data if needed
                try:
                    generate_response = generateAi(field1, field2, field3, field4)
                    if checked_checkboxes:
                        del request.session['checked_checkboxes']
                except Exception as e:
                    print(e)
                    return redirect('homepage:errorPage')

                request.session['openai'] = generate_response

        return redirect('homepage:home')


class Homepage(View):
    template_name = "homepage.html"

    @method_decorator(login_required(login_url="authenticate:login"))
    def get(self, request):
        generate_response = request.session.get('openai')
        venn_diagram = request.session.get('venn_scopes')
        checked_checkboxes = request.session.get('checked_checkboxes')

        context = {
            "venn_scopes": venn_diagram,
            "generate_response": generate_response,
            "checked": checked_checkboxes
        }

        return render(request, self.template_name, context)

    def post(self, request):
        pass


def generateAi(field1, field2, field3, field4):
    openai.api_key = "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"

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{
        "role": "user",
        "content": f"List five problem statements where these three scopes intersect. The three scopes are:"
                   f"{field1}, {field2}, {field3}, make sure not to include the numbering for "
                   f"the problem statement. I do not need an explanation; just give me the problem statement "
                   f"directly and not in question form. Please make each problem statement unique Apply filter: {field4}"
                   f"Take note not to include the fields that we're passed in the generated problem statements. "
                   f"Please do not generate question type of problem statement."
    }])
    print(completion)
    response_list = completion.choices[0].message.content.split('\n')

    questions_dict = {}

    for i, question in enumerate(response_list, start=1):
        # Split each question and take the second part (after the dot)
        question_without_number = question.split('. ', 1)[1].strip()
        questions_dict[i] = question_without_number

    return questions_dict

def errorPage(request):
    return render(request, 'error.html')