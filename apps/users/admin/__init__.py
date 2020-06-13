from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.models import Group
from apps.users.models import CustomUser
from django import forms


class UserChangeForm(forms.ModelForm):
    password_new = forms.CharField(required=False)
    password_new_confirm = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def save(self, commit=True, *args, **kwargs):
        user = super(UserChangeForm, self).save(commit=False)
        new_password = self.cleaned_data['password_new']
        if new_password:
            new_password_confirm = self.cleaned_data['password_new_confirm']
            if new_password == new_password_confirm:
                user.set_password(self.cleaned_data['password_new'])
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        new_password = self.cleaned_data['password_new']
        if new_password:
            new_password_confirm = self.cleaned_data['password_new_confirm']
            if new_password == new_password_confirm:
                user.set_password(self.cleaned_data['password_new'])
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class UserAdmin(ModelAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    fieldsets = (
        ('Основные данные', {'fields': ('first_name', 'last_name', 'middle_name')}),
        ('Системные данные', {'fields': ('email', 'username', 'is_superuser', 'is_deleted')}),
        ('Изменение пароля', {'fields': ('password_new', 'password_new_confirm')})
    )


site.register(CustomUser, UserAdmin)
site.unregister(Group)
