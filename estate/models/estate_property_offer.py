
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import  UserError
from odoo.tools.translate import _


class estatepropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offers"
    _order = "price desc"

    price = fields.Float ('Offered Price')
    status = fields.Selection (
        string = 'Status',
        selection =[('draft', 'Draft'),('Accepted','accepted'), ('Refused', 'refused')],
        copy=False,
        default='draft'
        )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    create_date = fields.Datetime(required=True, readonly=True, default=lambda self: fields.Datetime.now())
    accepted = fields.Boolean(string='Accepted', default=False)

    def action_offer_accepted(self):
        self.write({'status':'Accepted'})
        self.property_id.write({'buyer_id': self.partner_id.id, 'selling_price': self.price, 'state':'Sold'})

    def action_offer_refused(self):
        self.write({'status':'Refused'})

    def accept_offer(self):
        #self.ensure_one()
        if self.property_id.state == 'Sold':
            raise UserError(_('This property has  already been sold.'))
        self.write({'status':'Accepted'})
        self.property_id.write({'buyer_id': self.partner_id.id, 'selling_price': self.price, 'state':'Offer Accepted'})




    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Datetime.from_string(record.create_date)
                record.date_deadline = (create_date + timedelta(days=record.validity)).strftime("%Y-%m-%d")

    def _inverse_date_deadline(self):
        for record in self:
            #if record.create_date and record.date_deadline:
                create_date = fields.Datetime.from_string(record.create_date)
                date_deadline = fields.Date.from_string(record.date_deadline)
                record.validity = (date_deadline - create_date.date()).days

    _sql_constraints = [
        ('positive_price', 'CHECK(price>0)', 'Offered Price must be positive')

        ]


    @api.constrains('status')
    def _check_accepted_offer(self):
        for offer in self:
            if  offer.status == 'Accepted':
                accepted_offer = offer.property_id.offer_ids.filtered(lambda r: r.status == 'Accepted' and r.id != offer.id)
                if  accepted_offer:
                    raise ValidationError(_('Offer has already been accepted'))





