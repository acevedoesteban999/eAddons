import { _t } from '@web/core/l10n/translation';
import { Dialog } from '@web/core/dialog/dialog';
import { useService } from '@web/core/utils/hooks';
import { Component, onWillStart, useState } from '@odoo/owl';
import { EFloat } from "../e_float/e_float";
import { EMonetary } from "../e_monetary/e_monetary";

export class GenericConfiguratorDialog extends Component {
    static template = 'e_product_generic.GenericConfiguratorDialog';
    static components = { Dialog, EFloat, EMonetary };
    static props = {
        edit: { type: Boolean },
        product_template_id: { type: Number },
        save: { type: Function },
        discard: { type: Function },
        close: Function,
    };

    setup() {
        this.dialog = useService('dialog');
        this.env.dialogData.dismiss = () => this.cancel();
        this.orm = useService('orm');
        this.dialogTitle = false,
        this.product_template = {},
        this.state = useState({
            generic_bill_material_ids: [],
            finalCost: 0,
            totalCost: 0,
            invalidConfirm: false,
            invalidFinalCost: false,
        });
        
        onWillStart(async () => {
            const data =  await this.orm.call(
                'product.template',
                'read',
                [this.props.product_template_id,["display_name",'currency_symbol','currency_position']],
            );
            
            this.product_template = data[0]

            this.dialogTitle = _t("Dynamic Bill of Material: %s", this.product_template.display_name);

            this.state.generic_bill_material_ids = await this.orm.call(
                'product.template',
                'get_generic_bill_material_ids',
                [this.props.product_template_id],
            );

            this.state.generic_bill_material_ids.forEach((gbm) => {
                gbm.qty = 1;
                gbm.invalid = false;
                gbm.final_cost = 0;
                gbm.standard_price = gbm.standard_price || 0;
                this._computeFinalCost(gbm,false)
            });
            this._computeTotals()
            this.state.finalCost = this.state.totalCost
        });
    }

    onchangeQty(value, generic_product) {
        generic_product.qty = value;
        this._computeFinalCost(generic_product);
    }

    get_index_generic_product(generic_product){
        return this.state.generic_bill_material_ids.indexOf(generic_product)
    }

    onchangeInvalid(invalid,generic_product){
        generic_product.invalid = invalid
        this._computeInvalidConfirm()
    }
    
    onchangeInvalidFinalCost(invalid){
        this.state.invalidFinalCost = invalid
        this._computeInvalidConfirm()
    }


    onchangeFinalCost(value, generic_product) {
        generic_product.final_cost = value;
        this._computeTotals();
    }

    _computeFinalCost(generic_product,computeTotals = true) { 
        generic_product.final_cost = generic_product.qty * generic_product.standard_price;
        if(computeTotals)
            this._computeTotals()
    }

    _computeTotals() {
        let syncTotals = this.state.totalCost == this.state.finalCost
            
        this.state.totalCost = this.state.generic_bill_material_ids.reduce((sum, product) => {
            return sum + (product.final_cost || 0);
        }, 0); 
        
        if(syncTotals)
            this.state.finalCost = this.state.totalCost
    }

    _computeInvalidConfirm() {
        this.state.invalidConfirm = this.state.generic_bill_material_ids.some(gbm => gbm.invalid === true) || this.state.invalidFinalCost;
    }

    updateFinalCost(value) {
        this.state.finalCost = value;
    }

    async confirm() {
        this.props.save({
            lines: this.state.generic_bill_material_ids,
            finalCost: this.state.finalCost,
        });
        this.props.close();
    }

    cancel() {
        this.props.close();
        this.props.discard()
    }
}