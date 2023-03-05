from typing import Any, Optional
import pandas as pd
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from textvisualization.forms import DataForm
from textvisualization.utils import read_file_by_file_extension, show_wordcloud


class WordCloudView(View):
    template_name = "textvisualization/wordcloudvisualization.html"

    def get_context_data(self) -> dict[str, Any]:
        """For storing our context"""
        context: dict[str, Any] = {"DataForm": DataForm()}
        return context

    def narration_chart_data(self, request: HttpRequest, data:
                             Optional[pd.DataFrame]) -> HttpResponse:
        """For displaying wordcloud"""
        context = self.get_context_data()
        wordcloud = show_wordcloud(data)
        context["wordcloud"] = wordcloud
        return render(request, self.template_name, self.get_context_data())

    def post(self, request: HttpRequest) -> HttpResponse:
        context = self.get_context_data()
        form = DataForm(request.POST, request.FILES)
        values: list[str] = []
        if form.is_valid():
            user_file = form.cleaned_data["file"]
            read_file = read_file_by_file_extension(user_file)
            if read_file is not None:
                for _, row in read_file.iterrows():
                    values.append(row["narration"])
                converted_to_string = " ".join(values)
                return self.narration_chart_data(request, converted_to_string)
        else:
            form = DataForm()
        return render(request, self.template_name, context)
