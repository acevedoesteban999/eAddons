/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { loadJS, loadCSS } from "@web/core/assets";

publicWidget.registry.WebsiteVideoPlayer = publicWidget.Widget.extend({
    selector: '.o_video_website_player',
    
    async start() {
        await this._super(...arguments);
        
        if (!window.Plyr) {
            await Promise.all([
                loadCSS("/e_video_content/static/src/library/plyr/plyr.css"),
                loadJS("/e_video_content/static/src/library/plyr/plyr.js")
            ]);
        }
        
        this.initPlayer();
    },
    
    initPlayer() {
        const videoEl = this.el.querySelector('video');
        if (!videoEl || !window.Plyr) return;
        
        if (this.player) {
            this.player.destroy();
        }
        
        this.player = new Plyr(videoEl, {
            controls: [
                'play-large', 'play', 'progress', 'current-time', 'duration',
                'mute', 'volume', 'captions', 'settings', 'pip', 'fullscreen'
            ],
            settings: ['captions', 'quality', 'speed'],
            iconUrl: '/e_video_content/static/src/library/plyr/plyr.svg',
            storage: { enabled: false },
            preload: 'metadata',
        });
    },
    
   
    destroy() {
        if (this.player) {
            this.player.destroy();
            this.player = null;
        }
        this._super(...arguments);
    },
});

export default publicWidget.registry.WebsiteVideoPlayer;