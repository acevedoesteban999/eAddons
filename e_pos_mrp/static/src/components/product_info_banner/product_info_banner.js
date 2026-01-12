import { ProductInfoBanner } from "@point_of_sale/app/components/product_info_banner/product_info_banner"
import { patch } from "@web/core/utils/patch";
import { onMounted } from '@odoo/owl';

patch(ProductInfoBanner.prototype,{
    setup(){
        super.setup()
        
        onMounted(async()=>{
            const qty_data = await this.pos.data.call(
                "product.product",
                "read",
                [[this.props.product.raw.id], ["has_create_pos_mrp"]]
            );
            this.has_create_pos_mrp = qty_data[0]?.has_create_pos_mrp || false
        })
    },
})