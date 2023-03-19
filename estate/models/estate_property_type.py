
from odoo import fields, models

class estatepropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property types"
    _order = "sequence, name"

    name = fields.Char('Type of Property', required=True)
    sequence = fields.Integer('Sequence')

    property_ids = fields.One2many("estate.property","estate_property_type_id","Properties")
