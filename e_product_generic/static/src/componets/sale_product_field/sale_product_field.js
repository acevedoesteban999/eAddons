/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { SaleOrderLineProductField } from "@sale/js/sale_product_field";
import { GenericConfiguratorDialog } from "../generic_configurator_dialog/generic_configurator_dialog";
import { uuid } from "@web/views/utils";

patch(SaleOrderLineProductField.prototype, {
    async isGeneric() {
        const response =  await this.orm.call(
            'product.template',
            'read',
            [this.props.record.data.product_template_id[0] , ["generic_ok"]],
        )
        return response[0]?.generic_ok || false; 
    },   
    async onEditConfiguration() {
        if(await this.isGeneric() )
            this._openGenericConfiguration(true)
        else
            super.onEditConfiguration()
    },

    async _onProductTemplateUpdate(){
        if( await this.isGeneric() )
            this._openGenericConfiguration()
        else
            super._onProductTemplateUpdate()
    },

    async _openGenericConfiguration(edit=false){
        const saleOrder = this.props.record.model.root.data;
        const saleOrderRecord = this.props.record;

        this.dialog.add(GenericConfiguratorDialog, {
            edit: edit,
            product_template_id: this.props.record.data.product_template_id[0],
            save: async (vals)=>{
                saleOrder.order_line.leaveEditMode();
                const GenericLineValues = {
                    price_unit: vals.finalCost,
                };

                if (!edit) 
                    GenericLineValues.virtual_id = uuid();
                
                await saleOrderRecord.update(GenericLineValues);
                await saleOrder.order_line._sort();
            },
            discard: () => {
                saleOrder.order_line.delete(saleOrderRecord);
            },
        });
    },
});