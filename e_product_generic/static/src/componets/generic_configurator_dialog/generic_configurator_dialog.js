import { _t } from '@web/core/l10n/translation';
import { Dialog } from '@web/core/dialog/dialog';
import { useService } from '@web/core/utils/hooks';
import { Component, onWillStart, useState } from '@odoo/owl';
import { EFloatField } from "../e_float_field/e_float_field"

export class GenericConfiguratorDialog extends Component {
    static template = 'e_product_generic.GenericConfiguratorDialog';
    static components = { Dialog , EFloatField };
    static props = {
        edit: { type: Boolean },
        product_template_id: { type: Number },
        product_template_name: { type: String },
        save: { type: Function },
        discard: { type: Function },
        close: Function, // This is the close from the env of the Dialog Component
    };

    setup() {
        this.dialog = useService('dialog');
        this.env.dialogData.dismiss = () => this.cancel();
        this.orm = useService('orm')
        this.state = useState({
            generic_bill_material_ids: [],
        });
        onWillStart(async () => {
            this.state.generic_bill_material_ids = await this.orm.call(
                'product.template',
                'get_generic_bill_material_ids',
                [this.props.product_template_id],
            );

            this.state.generic_bill_material_ids.forEach((gbm) => {
                gbm['qty'] = 0;
                gbm['final_cost'] = 0;
            })
        });
    }
    onchangeQty(value,generic_product){
        generic_product.qty = value;
        this._computeFinalCost(generic_product);
    }

    _computeFinalCost(generic_product){
        generic_product.final_cost = generic_product.qty * generic_product.standard_price;
    }
    
    async confirm() {
        this.props.close();
    }

    cancel() {
        this.props.close();
    }

}
