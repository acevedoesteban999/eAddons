import { _t } from "@web/core/l10n/translation";
import { ProductConfiguratorDialog } from "@sale/js/product_configurator_dialog/product_configurator_dialog";
import { patch } from "@web/core/utils/patch";
import { onWillStart, useState } from '@odoo/owl';
import { useService } from "@web/core/utils/hooks";

patch(ProductConfiguratorDialog, {
    props: {
        ...ProductConfiguratorDialog.props,
        record : {type: Object, optional: true}
    }
})

patch(ProductConfiguratorDialog.prototype,{
    setup(){
        super.setup()
        this.orm = useService('orm')
        this.state.design = {}
        
        onWillStart(async ()=>{
            const res = await this.orm.call(
                'product.template',
                'read',
                [this.props.productTemplateId,['design_ok','design_ids']]
            )
            this.has_design = res[0]?.design_ok && res[0]?.design_ids.length > 0 
            if(this.has_design){
                const res1 =await this.orm.call(
                    'product.edesign',
                    'read',
                    [res[0]?.design_ids,['display_name','image']]
                )
                this.designs = res1
                if( this.props.record.data.design_id)
                    this.onChangeDesign({target:{value:this.props.record.data.design_id[0]}})
            }
        })
    },
    onChangeDesign(ev){
        const designId = Number(ev.target.value);
        if (!designId){          
            this.state.design = {};
        }else{
            const design = this.designs.find(v => v.id === designId);
            this.state.design = design;
        }
    },
    async onConfirm(options) {
        await super.onConfirm(options)
        if(this.has_design && this.state.design)
            this.props.record.update({
                design_id: [this.state.design.id , this.state.design.display_name],
            })
    }
})
