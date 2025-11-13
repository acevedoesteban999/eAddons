/** @odoo-module **/

import { Component , onWillStart , onMounted , useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { loadCSS , loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

  export class ProductComponent extends Component {
      static template = "e_sublimation.ProductComponent";
      static components = {};
      static props = {};

      setup() {
        console.log("A")
        this.state = useState({
          'products':[],
        
        });
        this.orm = useService('orm');
  
        onWillStart(async () => {
          await this.getData();
          await loadCSS('https://cdn.jsdelivr.net/npm/lightgallery@2.9.0/css/lightgallery-bundle.min.css');
          await loadJS('https://cdn.jsdelivr.net/npm/lightgallery@2.9.0/lightgallery.umd.min.js')
        });
  
        onMounted(() => {
          lightGallery(document.getElementById('animated-thumbnails'), {
            selector: '.lg-item',
            thumbnail: true,
            animateThumb: true,
            showThumbByDefault: false
          });
        
          
        });
      }

      async getData(){
        this.state.products = await this.orm.searchRead(
          'product.template',
          [
            ['sublimation_ok','=',true],
            ['product_tmpl_sublimation_id','!=',false],
          ],
          ['name','id','attachment_ids']
        )
      }
  }

  registry.category("public_components").add("e_sublimation.ProductComponent", ProductComponent);
  