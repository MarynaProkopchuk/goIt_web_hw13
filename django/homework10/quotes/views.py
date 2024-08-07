from .utils import get_database
from django.core.paginator import Paginator
from bson import ObjectId

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AuthorForm, QuoteForm


def main(request, page=1):
    db = get_database()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def author_detail(request, author_id):
    db = get_database()
    author = db.authors.find_one({"_id": ObjectId(author_id)})

    return render(request, "quotes/author.html", context={"author": author})


class AddAuthorView(LoginRequiredMixin, View):
    template_name = "quotes/add_author.html"
    form_class = AuthorForm
    login_url = "users:signin"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Author added")
            return redirect("quotes:add_author")
        return render(request, self.template_name, {"form": form})


class AddQuoteView(LoginRequiredMixin, View):
    template_name = "quotes/add_quote.html"
    form_class = QuoteForm
    login_url = "users:signin"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Quote added")
            return redirect("quotes:add_quote")
        return render(request, self.template_name, {"form": form})
