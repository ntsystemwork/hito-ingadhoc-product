##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo import api, models, exceptions, _


class IrModelAccess(models.Model):

    _inherit = 'ir.model.access'

    @api.model
    def check(self, model, mode='read', raise_exception=True):
        if isinstance(model, models.BaseModel):
            assert model._name == 'ir.model', 'Invalid model object'
            model_name = model.model
        else:
            model_name = model

        # permitimos que si se llama con super user no haya restriccion por mas que no este en el grupo
        # esto, entre otras cosas, resuelve un error al ir a ver producto en ecommerce y tmb el caso
        # donde hay acciones automaticas sobre modelo product.product y se usa sale_quotation_products
        if self.env.is_superuser():
            return True

        if mode != 'read' and model_name in [
                'product.template', 'product.product']:
            if self.env['res.users'].has_group(
                    'product_management_group.group_products_management'):
                return True
            elif raise_exception:
                raise exceptions.AccessError(_(
                    "Sorry, you are not allowed to manage products."
                    "Only users with 'Products Management' level are currently"
                    " allowed to do that"))
            else:
                return False
        return super(IrModelAccess, self).check(
            model, mode=mode, raise_exception=raise_exception)
