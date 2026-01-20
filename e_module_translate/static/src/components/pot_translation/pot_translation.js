/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@owl";

export class PotTranslationDialog extends Component {
    static template = "ir_module_e_translate.PotTranslationDialog";
    static components = { Dialog };
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            keys: [],
            langs: [],
            translations: {}, // {lang: {key: value}}
        });
        this.loadData();
    }

    async loadData() {
        const moduleId = this.props.resId;
        const module = await this.orm.call(
            "ir.module.e_translate",
            "get_po_data"
            [moduleId],
        );
        if (module && module.length) {
            this.state.keys = module[0].pot_keys || [];
            this.state.langs = module[0].po_translations.map(l => l.name) || [];
        }
    }

    get columns() {
        return ["Source", ...this.state.langs];
    }

    get rows() {
        return this.state.keys.map(key => ({
            key,
            values: this.state.langs.map(lang => this.state.translations[lang]?.[key] || ""),
        }));
    }
}





registry.category("actions").add("pot_translation_dialog", PotTranslationDialog);