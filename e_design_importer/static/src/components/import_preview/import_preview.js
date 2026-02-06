/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState } from "@odoo/owl";

export class ImportPreview extends Component {
    static template = "e_design_import.ImportPreview";
    
    setup() {
        this.state = useState({
            expanded: new Set(),
        });
    }

    get data() {
        const value = this.props.record.data[this.props.name];
        return value || {
            categories: [],
            subcategories: [],
            designs: [],
            products: []
        };
    }

    get stats() {
        const data = this.data;
        return {
            categories: data.categories?.length || 0,
            subcategories: data.subcategories?.length || 0,
            designs: data.designs?.length || 0,
            products: data.products?.length || 0
        };
    }

    get categories() {
        const data = this.data;
        return (data.categories || []).map(cat => ({
            ...cat,
            subcategories: this.getSubcategories(cat.code),
            designs: this.getDesigns(cat.code)
        }));
    }

    getSubcategories(parentCode) {
        const data = this.data;
        return (data.subcategories || [])
            .filter(sub => sub.parent_code === parentCode)
            .map(sub => ({
                ...sub,
                designs: this.getDesigns(sub.code)
            }));
    }

    getDesigns(categoryCode) {
        const data = this.data;
        return (data.designs || []).filter(design => design.category_code === categoryCode);
    }

    toggleExpand(code) {
        if (this.state.expanded.has(code)) {
            this.state.expanded.delete(code);
        } else {
            this.state.expanded.add(code);
        }
    }

    isExpanded(code) {
        return this.state.expanded.has(code);
    }
}

ImportPreview.props = {
    ...standardFieldProps,
};

export const importPreview = {
    component: ImportPreview,
};

registry.category("fields").add("import_preview", importPreview);