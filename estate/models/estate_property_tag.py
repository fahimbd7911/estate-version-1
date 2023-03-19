

from odoo import fields, models

class estatepropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags"
    _order = "name"

    name = fields.Char('Type of tags', required=True)


    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Tag name must be unique')

        ]
