
from odoo import api, fields, models
from odoo.exceptions import  UserError
from odoo.tools.translate import _

class estate_property(models.Model):
    _name = "estate.property"
    _description = "Property table for the estate"
    _order = "id desc"



    name = fields.Char('Name of Property', required=True)
    description = fields.Text ('Description')
    postcode = fields.Char ('Postcode')
    date_availability = fields.Date ('Available From', copy=False)
    expected_price = fields.Float ('Expected Price', required=True)
    selling_price = fields.Float ('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer ('Bedrooms', default='2')
    living_area = fields.Integer ('Living Area (sqm)')
    facades = fields.Integer ('Facades')
    garage = fields.Boolean ('Garage', default=True)
    garden = fields.Boolean ('Garden', default=True)
    garden_area = fields.Integer (string='Garden Area (sqm)', attrs="{'invisible':[('garden','=',False)]}")
    garden_orientation = fields.Selection (
        string = 'Garden Orientation',
        selection =[('N','North'), ('s', 'South'), ('e','East'),('w','West')], attrs="{'invisible':[('garden','=',False)]}"
        )
    state = fields.Selection (
        string = 'Status',
        selection =[('New','new'), ('Offer Received', 'offer received'), ('Offer Accepted','Accepted Offer'),('Sold','sold'),('Canceled','cancel order')],
        default = 'New'
        )
    active = fields.Boolean(default=True)

    estate_property_type_id = fields.Many2one("estate.property.type", string='Property Type')
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    estate_property_tag_id = fields.Many2many("estate.property.tag", string='Property Tags')
    offer_ids = fields.One2many("estate.property.offer","property_id", string='Offers')
    total_area = fields.Float(compute='_compute_total_area', store=True)
    best_price = fields.Float(string="Best Price", compute='_compute_best_price', store=True)

    @api.model
    def _get_default_name(self):
        return "New Property"

    @api.model
    def create(self,  vals):
        if "name" not  in vals:
            vals["name"] = self.get_default_name()
        return super().create(vals)

    #def write(self, vals):
     #   res = super().write(vals)
      #  if "selling_price" in vals:
       #     self.state = "Sold"
        #return res

    def unlink(self):
        for record in self:
            if record.state not  in ("New", "Canceled"):
                raise ValueError("Cannot delete property that is not new or canceled")
        return super().unlink()

    @api.model
    def create_offer(self, vals):
        property_id = val.get("property_id")
        property_obj = self.env["estate.property"].browse(property_id)
        if property_obj:
            existing_offers = property_obj.offer_ids.filtered(lambda r: r.price >= vals.get("price"))
            if existing_offers:
                raise ValueError("An existing offer has more or equal price")
            vals["state"] = "Offer Received"
            return property_obj.offer_ids.create(vals)
        return False

    def action_cancel(self):
        if self.state == 'Sold':
            raise UserError(_("You cannot cancel a property that has been sold."))
        self.write({'state':'Canceled'})

    def action_sold(self):
        if self.state == 'Canceled':
            raise UserError(_("You cannot set a  canceled  property as sold"))
        self.write({'state': 'Sold'})



    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = "0.0"


    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = "10"
            self.garden_orientation = "N"
        else:
            self.garden_area = "0"
            self.garden_orientation = False

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price>0)', 'Expected Price must be positive'),
        ('positive_selling_price', 'CHECK(selling_price>0)', 'Selling Price must be positive'),
        #('percentage_selling_price', 'CHECK(selling_price>(0.9*expected_price))','Selling Price must be atleast 90% of expected price')

        ]

    #@api.constrains('expected_price','selling_price')
    #def _check_property_prices(self):
      #  for record in self:
       #     if record.selling_price and record.selling_price < (0.9 * record.expected_price):
        #        raise  models.ValidationError (_('The selling price cannot be lower than 90% of the expected price'))

    class ResUsers(models.Model):
        _inherit = "res.users"

        property_ids = fields.One2many("estate.property","seller_id", string='Properties', domain=[('state','in',('New'))])








