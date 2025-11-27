/** @odoo-module **/

  import { Component } from "@odoo/owl";
  // import { registry } from "@web/core/registry";

  export class Breadcrumb extends Component {
      static template = "e_website_design.Breadcrumb";
      static props = [
        'back_url','breadcrumbs',
      ]
      // {
      //   back_url: String,
      //   breadcrumbs: 
      //   {
      //     type: Array,
      //     element: {
      //       type: Object,
      //       shape: {
      //         name: String,
      //         href: [
      //           String,
      //           undefined
      //         ],
      //       }
      //     },

      //   }
      // }

      setup() {}
  }

  // registry.category("public_components").add("e_website_design.Breadcrumb", Breadcrumb);
  