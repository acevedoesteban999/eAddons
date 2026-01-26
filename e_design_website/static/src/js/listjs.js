/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { loadJS } from "@web/core/assets";

publicWidget.registry.ListJs = publicWidget.Widget.extend({
    selector: '#listjs-search-component, [data-listjs]',
    async willStart() {
        await loadJS("/e_design_website/static/src/lib/listjs/listjs.js");
    },
    start: function() {
        this._super.apply(this, arguments);
        
        this.listjs = new List(this.el.id, {
            valueNames: this.el.dataset.valueNames ? JSON.parse(this.el.dataset.valueNames) : ['listjs-name']
        });
    },
});