from django.forms.widgets import Select, SelectMultiple
from django.utils.safestring import mark_safe

class CustomSelectWithQueryset(Select):
    '''
    Works with ModelChoiceField
    '''
    def __init__(self, queryset=None, attrs=None, choices=(), ajax_url=None):
        super().__init__(attrs=attrs, choices=choices)
        self.queryset = queryset
        self.ajax_url = ajax_url

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        # Set the id attribute based on the field name
        attrs['id'] = f'id_{name}'
        
        # Generate options from the queryset
        if self.queryset is not None:
            choices = [(obj.pk, str(obj)) for obj in self.queryset]
        else:
            choices = self.choices

        self.choices = choices
        print(self.choices)
        output = super().render(name, value, attrs, renderer)
        ajax_url = self.ajax_url
        # Add the Select2 initialization script
        script = f'''
            <script type="text/javascript">
                (function($) {{
                    $(document).ready(function() {{
                        $('#{attrs['id']}').select2({{
                            ajax: {{
                                url: '{ajax_url}',
                                dataType: 'json',
                                delay: 250,
                                data: function (params) {{
                                    return {{
                                        search: params.term,
                                        type: 'public'
                                    }};
                                }},
                                processResults: function (data) {{
                                    return {{
                                        results: $.map(data.results, function (item) {{
                                            return {{
                                                id: item.id,
                                                text: item.text
                                            }};
                                        }})
                                    }};
                                }},
                                cache: true
                            }},
                            placeholder: "Select option",
                            allowClear: true,
                        }});
                    }});
                }})(jQuery);
            </script>
        '''
        
        return mark_safe(output + script)
    


class CustomSelectMultipleWithUrl(SelectMultiple):
    '''
    Works with ModelMultipleChoiceField
    '''
    def __init__(self, queryset=None, attrs=None, choices=(), ajax_url=None):
        super().__init__(attrs=attrs, choices=choices)
        self.queryset = queryset
        self.ajax_url = ajax_url

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        # Set the id attribute based on the field name
        attrs['id'] = f'id_{name}'
        
        # Generate options from the queryset
        if self.queryset is not None:
            choices = [(obj.pk, str(obj)) for obj in self.queryset]
        else:
            choices = self.choices

        self.choices = choices
        output = super().render(name, value, attrs, renderer)
        
        # Add the Select2 initialization script with dynamic AJAX URL
        ajax_url = self.ajax_url
        script = f'''
            <script type="text/javascript">
                (function($) {{
                    $(document).ready(function() {{
                        $('#{attrs['id']}').select2({{
                            ajax: {{
                                url: '{ajax_url}',
                                dataType: 'json',
                                delay: 250,
                                data: function (params) {{
                                    return {{
                                        search: params.term,
                                        type: 'public'
                                    }};
                                }},
                                processResults: function (data) {{
                                    return {{
                                        results: $.map(data.results, function (item) {{
                                            return {{
                                                id: item.id,
                                                text: item.text
                                            }};
                                        }})
                                    }};
                                }},
                                cache: true
                            }},
                            placeholder: "Select options",
                            allowClear: true,
                            multiple: true  // Enable multiple selection
                        }});
                    }});
                }})(jQuery);
            </script>
        '''
        
        return mark_safe(output + script)