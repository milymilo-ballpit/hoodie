from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field, addon_classes=""):
    css_class = addon_classes + " "
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class += "is-invalid"
        elif (
            field_type(bound_field) != "PasswordInput"
            and isinstance(bound_field.value(), str)
            and bound_field.value().strip() != ""
        ):
            css_class += "is-valid"
        else:
            css_class += "is-valid"

    return css_class
