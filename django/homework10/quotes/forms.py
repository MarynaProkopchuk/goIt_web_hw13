from django import forms
from .models import Author, Quote, Tag


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(forms.ModelForm):
    tags = forms.CharField(help_text="Write the tag")

    class Meta:
        model = Quote
        fields = ["author", "quote", "tags"]

    def save(self, commit=True):
        quote = super().save(commit=False)
        tags_str = self.cleaned_data["tags"]
        tags = [tag.strip() for tag in tags_str.split(",")]
        if commit:
            quote.save()
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)
        return quote
