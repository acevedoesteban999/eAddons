/** @odoo-module **/

import { Component , onWillStart , useState , useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
//import { loadCSS , loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { SearchComponent } from "../search/search"
import { removeLoader } from "../../../js/public_designs"

  export class CatalogDesignsComponent extends Component {
      static template = "e_website_design.CatalogDesignsComponent";
      static components = {SearchComponent};
      static props = ['product_id?']

      setup() {
          this.state = useState({
            'designs': [],
            'category': false,
          })
          this.buttonCloseFilter = useRef('buttonCloseFilter')
          this.orm = useService('orm')
          
          onWillStart(async ()=>{
              await this.searchDesigns();
              removeLoader()
          })
      }

      async searchDesigns(){
        let domain = [];
        if (this.props.product_id)
          domain.push(['product_ids','=',this.props.product_id]);
        if (this.state.category)
          domain.push(['category_id','=',this.state.category.id]);
        
        this.state.designs = await this.orm.searchRead(
          'product.design',
          domain,
          ['id','name','default_code']
        );
      }

      onSelectCategory(category){
        this.state.category = category;
        this.searchDesigns().then(()=>{
          this.buttonCloseFilter.el.click() 
        })
      }

      onSelectDesign(design){
        
      }



  }

  registry.category("public_components").add("e_website_design.CatalogDesignsComponent", CatalogDesignsComponent);
  