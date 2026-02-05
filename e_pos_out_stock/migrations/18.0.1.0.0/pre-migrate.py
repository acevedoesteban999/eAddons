import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Starting ePosOutStock migration: 18.0.1.0.0")
    
    view = env.ref('e_pos_out_stock.e_pos_out_stock_res_config_settings_view_form_pos_invoice_toggle', raise_if_not_found=False)
    if view:
        _logger.info(f"Deleting inherited view: ID={view.id}, Name={view.name}")
        view.unlink()
        _logger.info("View deleted successfully")
    else:
        _logger.info("Inherited view not found")
    
    group = env.ref('ePosOutStock.group_hide_out_stock', raise_if_not_found=False)
    if group:
        _logger.info(f"Deleting security group: ID={group.id}, Name={group.name}")
        group.unlink()
        _logger.info("Security group deleted successfully")
    else:
        _logger.info("Security group not found")
    try:
        cr.execute("""
            DELETE FROM ir_model_fields 
            WHERE name = 'group_hide_out_stock' 
            AND model = 'res.config.settings'
        """)
        
        if cr.rowcount > 0:
            _logger.info(f"Deleted {cr.rowcount} obsolete fields")
    except Exception as e:
        _logger.info(f"Error: {e}")
    _logger.info("Migration Finished")