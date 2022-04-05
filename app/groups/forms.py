from django import forms

from groups.models import Group, Event, Term


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class CreateGroupForm(forms.ModelForm):
    join_url = forms.URLField()
    location = forms.CharField(max_length=50)

    class Meta:
        model = Group
        fields = '__all__'
        exclude = [
            'slug', 'active', 'date_created',
            'date_updated', 'date_deleted'
        ]

    def save(self, *args, **kwargs):
        group = super(CreateGroupForm, self).save(*args, **kwargs)
        try:
            Term.objects.create(
                group=group,
                join_url=self.cleaned_data['join_url'],
                location=self.cleaned_data['location']
            )
        except Exception as e:
            group.delete()


class UpdateGroupForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ('join_url', 'location')


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['is_cancelled', 'date_deleted']
        widgets = {
            'start_time': DateTimeInput(),
            'end_time': DateTimeInput()
        }
