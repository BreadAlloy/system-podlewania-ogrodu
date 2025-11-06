from django.template.response import TemplateResponse
from django.views import generic

# Class based views
class InheritanceTestView(generic.TemplateView):
    template_name = "company/test.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["tests"] = ["test1", "test2", "test3"]
    #     return context

class PureTestView(generic.View):

    def get(self, request, *args, **kwargs):
        # return TemplateResponse(request, "company/test.html", context={"member_pk": self.kwargs.get("member_pk")})
        return TemplateResponse(request, "company/test.html")

# Function based views, moja opinia ale na zajęciach nie używamy.
def function_based_view(request):
  return TemplateResponse(request, "company/function_test.html")



#######################################

TEAM_DATA = [
    {'name': 'Jan Kowalski', 'position': 'CEO', 'slug': 'jan-kowalski'},
    {'name': 'Anna Nowak', 'position': 'CTO', 'slug': 'anna-nowak', 'is_senior': True},
    {'name': 'Piotr Pawlak', 'position': 'Developer', 'slug': 'piotr-pawlak'},
]


class HomeView(generic.TemplateView):
    template_name = "company/home.html"

class AboutView(generic.TemplateView):
    template_name = "company/about.html"

class TeamView(generic.TemplateView):
    template_name = "company/team.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = TEAM_DATA
        return context

class TeamMemberView(generic.TemplateView):
    template_name = "company/member_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for data in TEAM_DATA:
            if data['slug'] == kwargs.get("team_member"):
                context["member_detail"] = data
                return context

        context["member_detail"] = {'error': "cant find"}
        return context