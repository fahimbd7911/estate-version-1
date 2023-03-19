from  odoo import  models,  api, exceptions

class EstateProperty(models.Model):
    _inherit = "estate.property"



    def action_sold(self):
        res = super().action_sold()
        print("Customm method called")
        journals = self.env["account.journal"].search([("type", "=", "sale")])
        if len(journals)<=0:
            raise exceptions.ValidationError("No sale journal found")
        journal=journals[0]
        for  property_record in self:
            invoice_values = {
                'partner_id': property_record.buyer_id.id,
                'move_type':'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids':[
                    (0, 0,{
                        'name':'Property Sold',
                        'quantity': 1,
                        'price_unit': property_record.selling_price * 0.06,
                        }),
                    (0, 0,{
                        'name': 'Adminstrative fees',
                        'quantity': 1,
                        'price_unit': 100,
                     }),

                    ],
                }
            invoice = self.env['account.move'].create(invoice_values)
        return  res



   # def action_sold(self):
   #     res = super().action_sold()
    #    for  property_record in self:
     #       partner_id = property_record.buyer_id.id
      #      move_vals ={
       #         'move_type':'out_invoice',
        #        'partner_id':partner_id,
         #   }
          #  invoice = self.env['account.move'].create(move_vals)
           # price = property_record.price
         #   fee = "100"
         #   tax_rate = "0.06"
         #   tax = price * tax_rate
         #   lines = [
          #      (0,0,{
           #         'name': property_record.name,
            #        'quantity': 1,
             #       'price_unit': price * (1 + tax_rate),
             #       'tax_ids':[(6, 0, [self.env.ref('account.account_tax_6').id])],
              #  }),
              #  (0, 0, {
               #     'name': 'Administration fees',
                #    'quantity': 1,
                 #   'price_unit': fee,
                 #   'tax_ids':[(6, 0, [])],

               # })

            #]
         #   invoice.write({'invoice_line_ids': lines})
         #   invoice.action_post()
       # return res

