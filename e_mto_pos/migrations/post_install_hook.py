import logging
_logger = logging.getLogger(__name__)

def post_install_hook(env):
    _logger.info("Starting e_mto_pos installation")
    cr = env.cr
    cr.execute("""
        SELECT EXISTS(
            SELECT 1 FROM information_schema.tables 
            WHERE table_name = 'z_temp_pos_mrp_data'
              AND table_schema = 'public'
        )
    """)
    
    result = cr.fetchone()
    if not result or not result[0]:
        _logger.info("No temporary table from e_pos_mrp found, nothing to migrate")
        return
    
    _logger.info("Found temporary table z_temp_pos_mrp_data")
    
    cr.execute("SELECT COUNT(*) FROM public.z_temp_pos_mrp_data")
    total_en_tabla = cr.fetchone()[0]
    
    if total_en_tabla == 0:
        _logger.info("Temporary table exists but is empty, nothing to migrate")
        cr.execute("DROP TABLE public.z_temp_pos_mrp_data")
        return
    
    _logger.info("Found %s records to migrate", total_en_tabla)
    
    cr.execute("""
        UPDATE product_template pt
        SET can_create_mto_pos = t.can_create_pos_mrp
        FROM public.z_temp_pos_mrp_data t
        WHERE pt.id = t.product_template_id
          AND t.can_create_pos_mrp IS NOT NULL
    """)
    
    migrados = cr.rowcount
    _logger.info("Migrated %s records to can_create_mto_pos", migrados)
    
    cr.execute("""
        SELECT t.product_template_id 
        FROM public.z_temp_pos_mrp_data t
        LEFT JOIN product_template pt ON pt.id = t.product_template_id
        WHERE pt.id IS NULL
    """)
    
    huerfanos = cr.fetchall()
    if huerfanos:
        _logger.warning("%s orphaned records found: %s", len(huerfanos), [h[0] for h in huerfanos])
    
    cr.execute("DROP TABLE public.z_temp_pos_mrp_data")
    _logger.info("Temporary table dropped, migration completed")
    
    env['product.template'].invalidate_model(['can_create_mto_pos'])
    env['product.product'].invalidate_model(['has_create_mto_pos'])  