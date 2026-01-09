/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    async afterProcessServerData() {
        const res = await super.afterProcessServerData?.(...arguments);

        const products = this.models["product.product"].getAll();
        if (!products.length) return res;

        const product_ids = products.map(p => p.id);

        try {
            const qty_data = await this.data.call(
                "product.product",
                "read",
                [product_ids, ["qty_available","can_show_in_pos_out_stock"]]
            );

            qty_data.forEach((prod) => {
                const localProd = this.models["product.product"].get(prod.id);
                if (localProd){
                    localProd.raw.qty_available = prod.qty_available ?? 0;
                    localProd.raw.can_show_in_pos_out_stock = prod.can_show_in_pos_out_stock ?? false;
                } 
            });

            
        } catch (err) {}

        return res;
    },
});