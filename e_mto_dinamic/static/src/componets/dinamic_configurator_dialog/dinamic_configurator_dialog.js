import { _t } from '@web/core/l10n/translation';
import { Dialog } from '@web/core/dialog/dialog';
import { useService } from '@web/core/utils/hooks';
import { Component, onWillStart, useState } from '@odoo/owl';
import { EFloat } from "../e_float/e_float";
import { EMonetary } from "../e_monetary/e_monetary";

export class DinamicConfiguratorDialog extends Component {
    static template = 'e_mto_dinamic.DinamicConfiguratorDialog';
    static components = { Dialog, EFloat, EMonetary };
    static props = {
        product_template_id: { type: Number },
        finalCost : { type: Number , optional: true},
        dinamic_bill_material_data : { type: Array , optional: true},
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
            dinamic_bill_material_data:  [],
            finalCost: this.props.finalCost || 0,
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
            let edit = this.props.dinamic_bill_material_data && this.props.dinamic_bill_material_data.length
            if(edit)
                this.state.dinamic_bill_material_data = this.props.dinamic_bill_material_data
            else{
                this.state.dinamic_bill_material_data = await this.orm.call(
                    'product.template',
                    'get_dinamic_bill_material_data',
                    [this.props.product_template_id],
                );
                this.state.dinamic_bill_material_data.forEach((gbm) => {
                    gbm.qty = 1;
                    gbm.invalid = false;
                    gbm.subtotal_cost = 0;
                    gbm.standard_price = gbm.standard_price || 0;
                    this._computeLineTotalCost(gbm,false)
                });
            }
            this._computeTotals(edit)
            
            
        });
    }

    onchangeQty(value, dinamic_product) {
        dinamic_product.qty = value;
        this._computeLineTotalCost(dinamic_product);
    }

    onchangeInvalid(invalid,dinamic_product){
        dinamic_product.invalid = invalid
        this._computeInvalidConfirm()
    }
    
    onchangeInvalidFinalCost(invalid){
        this.state.invalidFinalCost = invalid
        this._computeInvalidConfirm()
    }


    onchangeFinalCost(value, dinamic_product) {
        dinamic_product.subtotal_cost = value;
        this._computeTotals();
    }

    _computeLineTotalCost(dinamic_product,computeTotals = true) { 
        dinamic_product.subtotal_cost = dinamic_product.qty * dinamic_product.standard_price;
        if(computeTotals)
            this._computeTotals()
    }

    _computeTotals(computeSubTotals = false) {
        if(computeSubTotals)
            this.state.dinamic_bill_material_data.forEach((gbm) => {
                this._computeLineTotalCost(gbm,false)
            });

        let syncTotals = this.state.totalCost == this.state.finalCost
            
        this.state.totalCost = this.state.dinamic_bill_material_data.reduce((sum, product) => {
            return sum + (product.subtotal_cost || 0);
        }, 0); 
        
        if(!this.state.finalCost || syncTotals)
            this.state.finalCost = this.state.totalCost
    }

    _computeInvalidConfirm() {
        this.state.invalidConfirm = this.state.dinamic_bill_material_data.some(gbm => gbm.invalid === true) || this.state.invalidFinalCost;
    }

    updateFinalCost(value) {
        this.state.finalCost = value;
    }

    async confirm() {
        this.props.save({
            dinamic_bill_material_data: this.state.dinamic_bill_material_data.map(
                ({ invalid,subtotal_cost, ...rest }) => rest
            ),
            finalCost: this.state.finalCost,
        });
        this.props.close();
    }

    cancel() {
        this.props.close();
        this.props.discard()
    }
}