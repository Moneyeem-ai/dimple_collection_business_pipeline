

class SideBarSelectedMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = self.parent
        context['segment'] = self.segment
        return context
