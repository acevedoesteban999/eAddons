import { _t } from "@web/core/l10n/translation";
import { formatFloat } from "@web/views/fields/formatters";
import { parseFloat } from "@web/views/fields/parsers";
import { Component, useState } from "@odoo/owl";

export class EFloatField extends Component {
    static template = "e_product_generic.EFloatField";
    static props = {
        readonly: { type: Boolean, optional: true },
        value: { type: Number, optional: true },
        digits: { type: Array, optional: true },
        update: { type: Function },
        class : { type : String , optional: true}
    };
    
    setup() {
        this.state = useState({
            hasFocus: false,
            isInvalid: false,
            inputValue: this.formatValue(this.props.value),
        });
    }

    get displayValue() {
        return this.state.hasFocus ? this.state.inputValue : this.formatValue(this.props.value);
    }

    get formattedValue() {
        return this.formatValue(this.props.value);
    }

    formatValue(value) {
        if (value === false || value === null || value === undefined) {
            return "";
        }
        return formatFloat(value, { digits: this.props.digits });
    }

    onInput(ev) {
        const inputValue = ev.target.value;
        this.state.inputValue = inputValue;
        
        try {
            const parsedValue = parseFloat(inputValue);
            this.state.isInvalid = false;
            this.props.update(parsedValue);
        } catch (error) {
            this.state.isInvalid = true;
        }
    }
}