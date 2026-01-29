/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, onWillStart, useState } from "@odoo/owl";
export class PotTranslationDialog extends Component {
    static template = "ir_module_e_translate.PotTranslationDialog";
    static components = { Dialog };
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            datas: {},
        });
        onWillStart(async()=>{
            await this.loadData();
        })
    }

    async loadData() {
        this.state.datas = await this.orm.call(
            "ir.module.e_translate",
            "get_pot_translation_data",
            [this.props.action.context.e_translate_id],
        );
    }

    
}





registry.category("actions").add("pot_translation_dialog", PotTranslationDialog);