import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype,{
    can_be_merged_with(orderline){
        return super.can_be_merged_with(orderline) && (orderline.design_id?.id === this.raw.design_id?.id )
    },
    getDisplayData() {
        let data = super.getDisplayData()
        return {
            ...data,
            design_id: this.raw.design_id?{'name':this.raw.design_id.name}:false
        }
    }
})
