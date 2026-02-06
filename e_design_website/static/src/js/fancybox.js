/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.DivHref = publicWidget.Widget.extend({
    selector: '.fancybox-item',
    
    start: function() {
        this._super.apply(this, arguments);
        
        Fancybox.bind('[data-fancybox="gallery"]', {
            Toolbar: {
            display: [
                { id: "counter", position: "center" },
                "zoom",
                "fullscreen",
                "close",
            ],
            },
        });
    },
});