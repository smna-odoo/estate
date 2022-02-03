from odoo import models, fields

class resPartner(models.Model):
    _inherit = 'res.partner'
    
    offer_ids = fields.One2many('estate.property.offer', 'partner_id')
    is_buyer = fields.Boolean(string="Is Buyer")
    
    