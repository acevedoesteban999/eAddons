/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { loadCSS , loadJS } from "@web/core/assets";

export class CatalogComponent extends Component {
    static template = "e_sublimation.CatalogComponent";
    static components = {};
    static props = {};

    setup() {
      onWillStart(async () => {
        await loadCSS('https://cdn.jsdelivr.net/npm/@splidejs/splide@4.1.4/dist/css/splide.min.css');
        await loadJS('https://cdn.jsdelivr.net/npm/@splidejs/splide@4.1.4/dist/js/splide.min.js')
      });
      onMounted(() => {
          
      });

    }
}

registry.category("public_components").add("e_sublimation.catalogComponent", CatalogComponent);
  