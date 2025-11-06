from django.contrib import admin
from django.urls import path, include

from apps.company.views import InheritanceTestView, PureTestView, function_based_view, HomeView, AboutView, TeamView, TeamMemberView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("inheritance_test/<int:member_pk>/", InheritanceTestView.as_view(), name="inheritance_test"),
    path("pure_test/<int:member_pk>/", PureTestView.as_view(), name="pure_test"),
    path("function_based_view/", function_based_view, name="function_based_view"),

    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("team/", TeamView.as_view(), name="team"),
    path("team/<slug:team_member>/", TeamMemberView.as_view(), name="teammember")
]
