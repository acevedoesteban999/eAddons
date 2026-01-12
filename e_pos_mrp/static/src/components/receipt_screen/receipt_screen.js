import { patch } from "@web/core/utils/patch";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { _t } from "@web/core/l10n/translation";
import { onMounted } from "@odoo/owl";

patch(ReceiptScreen.prototype,{
    async _get_hasPicking(order_id){
          return await this.pos.data.call(
            "stock.picking",
            "read_picking_by_pos_order",
            [],
            {pos_order_id: order_id}
        ); 
    },
    setup(){
        super.setup()
        this.state.picking_id = false
        this.state.pos_order_id = false
        onMounted(async () => {
            const order = this.pos.get_order();
            this.state.picking_id = await this._get_hasPicking(order?.id||null)
            this.state.pos_order_id = order
        });


    }
})