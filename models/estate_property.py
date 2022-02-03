from odoo import _, api, models,fields
import datetime
from odoo.exceptions import UserError,ValidationError

class  EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type"
    _sql_constraints = [('unique_property_type_name', 'unique(name)', 'Type cannot be duplicated')]

    name = fields.Char()
    property_id = fields.One2many('estate.property', 'property_type_id')

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _sql_constraints = [('positive_check', 'check(expected_price > 0)', 'Enter positive value')]
    _order = 'id desc'
    
    def _get_discription(self):
        # print(self.env.user.name)
        # if self.env.context.get('my_property_search'):
        return self.env.user.name + '\'s property'
    
    name = fields.Char(default = "Unknown",required = True)
    description = fields.Text(default=_get_discription)
    postcode = fields.Char()
    date_availability = fields.Date(default = lambda self: fields.Datetime.now(), copy= False)
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(copy= False, readonly = True)
    buyer = fields.Char()
    best_price  = fields.Float(readonly = True,compute="_compute_best_price")
    bedrooms = fields.Integer(default= 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
    	("North", "North"),
    	("South", "South"),
    	("East", "East"),
    	("West", "West")
    	])
    active = fields.Boolean(default=True)
    image = fields.Image()
    salesman = fields.Many2one('res.partner',default=lambda self: self.env.user)
    property_tags = fields.Many2many("estate.property.tags")
    property_type_id = fields.Many2one("estate.property.type")
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute="_compute_area",inverse="_inverse_area")
    valid_till = fields.Date(compute="_valid_days", inverse="_inverse_days")
    valid_days = fields.Integer(default=7)
    state = fields.Selection([
        ('new','New'),
        ('sold','Sold'),
        ('cancel','Cancel')
        ], default='new')
    
    # currency_id = fields.Many2one('res.currency', default= lambda self : self.env.company.currency_id)
    

    @api.onchange('garden')
    def _onchange(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "North"
            else:
                record.garden_area = 0
                record.garden_orientation = None


    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            max_price = 0
            for offer in record.property_offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price
    
    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    
    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2
          
    @api.depends('valid_days')
    def _valid_days(self):
        for record in self:
            record.valid_till = record.date_availability + datetime.timedelta(days=record.valid_days)
    
    def _inverse_days(self):
        for record in self:
            # a = date(record.valid_till.year, record.valid_till.month, record.valid_till.day)
            # b = date(record.date_availability.year, record.date_availability.month, record.date_availability.day)
            # d = a - b
            # print(d.days)
            # record.valid_days = d.days
            a=record.valid_till-record.date_availability
            record.valid_days=a.days
    
    # @api.constrains('expected_price')
    # def _check_instructor(self):
    #     if self.expected_price < 100:
    #         raise UserError(_("Please enter exected price greater than 100"))
    
    @api.constrains('living_area', 'garden_area')
    def _living_garden_check(self):
        for rec in self:
            if rec.garden_area > rec.living_area:
                raise ValidationError(_("garden cannot be bigger than living area"))
    
    def action_sold(self):
        for rec in self:
            if rec.state == 'cancel':
                raise UserError(_("Canceled property cannot be sold"))
            else:
                rec.state = 'sold'
            
    def action_cancel(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(_("sold property cannot be cancel"))
            else:
                rec.state = 'cancel'
    
    def open_offers(self):
        view_id = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id, 'tree']],
            # "res_id": 2,
            "target":"new",
            "domain": [('property_id', '=', self.id)]
            }
    
    # def hide_btn(self):
    #     for i in self:
    #         if i.state
            
class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'estate property tags'
    _sql_constraints = [('unique_property_type_name', 'unique(name)', 'Tag cannot be duplicated')]
    
    
    name = fields.Char()
    color = fields.Integer()
    

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    # _order = 'price desc'
    # _order = 'price asc'
    _rec_name = 'partner_id'


    price = fields.Float()
    partner_id = fields.Many2one('res.partner', domain="[('is_buyer','=',True)]")
    property_id = fields.Many2one('estate.property')
    property_type_ids = fields.Many2one(related='property_id.property_type_id', Store=True)
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refuse','Refused')
    ])
    
    
    def action_accepted(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.selling_price = rec.price
            rec.property_id.buyer = rec.partner_id
            print(rec.partner_id)
    
    def action_rejected(self):
        for rec in self:
            rec.status = 'refuse'


# class buyerDetais(models.Model):
#     _inherit = 'res.partner'
    
#     is_buyer = fields.Boolean()

    
    
    