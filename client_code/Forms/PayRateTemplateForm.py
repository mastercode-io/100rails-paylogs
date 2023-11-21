from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid


class PayRateTemplateForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRateTemplateForm')
        kwargs['model'] = 'PayRateTemplate'

        self.name = TextInput(name='name', label='Name')
        self.description = MultiLineInput(name='description', label='Description', rows=4)
        self.scope = LookupInput(name='scope', label='Scope', model='Scope')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')

        pay_rate_template_items_view = {
            'model': 'PayRateTemplateItem',
            'columns': [
                {'name': 'order_number', 'label': 'Order'},
                {'name': 'pay_rate_title', 'label': 'Title'},
                {'name': 'pay_rate_rule.name', 'label': 'Rule'},
                {'name': 'pay_rate', 'label': 'Rate'},
                {'name': 'pay_rate_multiplier', 'label': 'Multiplier'},
                {'name': 'status', 'label': 'Status'},
            ],
        }
        self.items = SubformGrid(name='items', label='Pay Rate Rules', model='PayRateTemplateItem',
                                 link_model='PayRateTemplate', link_field='pay_rate_template',
                                 form_container_id=kwargs.get('target'),
                                 view_config=pay_rate_template_items_view,
                                 )

        sections = [
            {
                'name': '_', 'cols': [
                    [self.name, self.scope],
                    [self.description, self.status],
            ]
            },
            {
                'name': '_', 'rows': [
                    [self.items],
            ]
            }
        ]

        super().__init__(sections=sections, **kwargs)
        self.fullscreen = True
