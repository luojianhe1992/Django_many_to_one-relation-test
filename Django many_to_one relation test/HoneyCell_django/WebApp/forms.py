from WebApp.models import *
from django import forms

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['reporter', 'headline', 'content', 'pub_date']
        widgets = {'headline': forms.TextInput(),
                   'content': forms.Textarea(),
                   'pub_date': forms.SelectDateWidget()}

    def clean(self):
        cleaned_date = super(ArticleForm, self).clean()

        reporter = self.cleaned_data.get('reporter')
        headline = self.cleaned_data.get('headline')
        content = self.cleaned_data.get('content')
        pub_date = self.cleaned_data.get('pub_date')

        return cleaned_date

    def clean_reporter(self):

        reporter = self.cleaned_data.get('reporter')

        if not reporter:
            print("Please type in the reporter.")
            raise forms.ValidationError("Please type in the reporter.")

        return reporter

    def clean_headline(self):

        headline = self.cleaned_data.get('headline')

        if not headline:
            print("Please type in the headline.")
            raise forms.ValidationError("Please type in the headline.")

        return headline

    def clean_content(self):

        content = self.cleaned_data.get('content')

        if not content:
            print("Please type in the content.")
            raise forms.ValidationError("Please type in the content.")

        return content

    def clean_pub_date(self):

        pub_date = self.cleaned_data.get('pub_date')

        if not pub_date:
            print("Please type in the pub_date.")
            raise forms.ValidationError("Please type in the pub_date.")

        return pub_date


