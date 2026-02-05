import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Starting ePosMrp migration: 18.0.1.0.1")
    
    view = env.ref('e_pos_mrp.pos_order_form_inherit_pos_order_form', raise_if_not_found=False)
    if view:
        _logger.info(f"Deleting inherited view: ID={view.id}, Name={view.name}")
        view.unlink()
        _logger.info("View deleted successfully")
    else:
        _logger.info("Inherited view not found")
    
    
    _logger.info("Migration Finished")