from abc import ABC, abstractmethod

class ChartViewBase(ABC):
    title = "Chart"
    form_class = None

    def get_form_prefix(self):
        return self.__class__.__name__.lower()

    def get_context_data(self, request):
        form = self.form_class(request.GET or None)
        form.is_valid()

        result = self.get_chart_data(form.cleaned_data if form.is_valid() else {})
        if len(result) == 3:
            labels, values, extras = result
        else:
            labels, values = result
            extras = {}

        # single series compatibility
        if values and isinstance(values[0], (int, float)):
            values = [{"label": self.title, "data": values}]

        return {
            "title": self.title,
            "form": form,
            "chart_labels": labels,
            "chart_values": values,
            "chart_extras": extras,
        }

    @abstractmethod
    def get_chart_data(self, filters: dict) -> tuple[list, list]:
        pass
