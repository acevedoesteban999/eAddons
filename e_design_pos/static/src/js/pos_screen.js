/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";


patch(ProductScreen.prototype, {
    get productsToDisplay() {
        let finalList = super.productsToDisplay;
        
        finalList = finalList.filter(p => Number(p.raw.qty_available || 0) > 0 || p.raw.can_show_in_pos_out_stock);
        
        return finalList;
    },
});

