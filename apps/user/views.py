from django.shortcuts import render


class IsUserAuthenticatedMixin:
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("work:work_review")
        form = self.form_class()
        return render(request, self.template_name, {"form": form})



