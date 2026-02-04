/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { FileUploader } from "@web/views/fields/file_handler";
import { loadJS, loadCSS } from "@web/core/assets";




export class VideoContentField extends Component {
    static template = "e_design_website.VideoContentField";
    static components = { FileUploader };
    static props = {
        ...standardFieldProps,
        filenameField: { type: String, optional: true },
    };

    setup() {
        this.state = useState({
            videoUrl: null,
            loading: false,
            libsLoaded: false,
            error: null,
        });
        this.content = null;
        this.contentRef = useRef("content");
        this.abortController = null;
        
        onMounted(() => this.init());
        onWillUnmount(() => this.destroy());
    }

    async init() {
        const recordId = this.props.record.resId;
        const fieldValue = this.props.record.data[this.props.name];
        
        if (!recordId || !fieldValue) {
            this.state.videoUrl = null;
            return;
        }

        // Siempre usa streaming URL
        this.state.videoUrl = `/e_design_website/video/stream/${recordId}`;
        this.state.loading = true;

        try {
            await this.loadPlyr();
            await this.initContent();
        } catch (error) {
            console.error("VideoContent init error:", error);
            this.state.error = "Failed to load video content";
        } finally {
            this.state.loading = false;
        }
    }

    async loadPlyr() {
        if (window.Plyr) {
            this.state.libsLoaded = true;
            return;
        }

        await Promise.all([
            loadCSS("/e_design_website/static/src/library/plyr/plyr.css"),
            loadJS("/e_design_website/static/src/library/plyr/plyr.js"),
        ]);
        
        this.state.libsLoaded = true;
    }

    async initContent() {
        if (!this.contentRef.el || !window.Plyr) return;

        if (this.content) {
            this.content.destroy();
            this.content = null;
        }

        this.content = new Plyr(this.contentRef.el, {
            controls: [
                'play-large', 'play', 'progress', 'current-time', 'duration',
                'mute', 'volume', 'captions', 'settings', 'pip', 'airplay', 'fullscreen'
            ],
            settings: ['captions', 'quality', 'speed', 'loop'],
            loadSprite: false,
            iconUrl: false,
            blankVideo: false,
            autoplay: false,
            preload: 'metadata',
            storage: { enabled: false },
            enableContextMenu: true,
            quality: {
                default: 1080,
                options: [4320, 2880, 2160, 1440, 1080, 720, 576, 480, 360, 240],
            },
            speed: {
                selected: 1,
                options: [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
            },
            keyboard: {
                focused: true,
                global: false,
            },
            tooltips: {
                controls: true,
                seek: true,
            },
            // Optimizaciones de buffer
            buffered: true,
            debug: false,
        });

        // Eventos de error y carga
        this.content.on('error', (event) => {
            console.error('Plyr error:', event.detail);
            this.state.error = "Video playback error";
        });

        this.content.on('loadedmetadata', () => {
            this.state.loading = false;
        });
    }

    destroy() {
        if (this.content) {
            try {
                this.content.destroy();
            } catch (e) {
                console.warn("Error destroying content:", e);
            }
            this.content = null;
        }
        
        if (this.abortController) {
            this.abortController.abort();
            this.abortController = null;
        }
    }

    get hasVideo() {
        return !!this.state.videoUrl;
    }

    get filename() {
        return this.props.record.data[this.props.filenameField] || "video.mp4";
    }

    async update({ data, name }) {
        this.destroy();
        
        if (!data) {
            this.state.videoUrl = null;
            return this.props.record.update({ 
                [this.props.name]: false,
                [this.props.filenameField]: false 
            });
        }

        try {
            await this.props.record.update({ 
                [this.props.name]: data, 
                [this.props.filenameField]: name 
            });
            
            await new Promise(resolve => setTimeout(resolve, 200));
            await this.props.record.load();
            
            this.init();
        } catch (error) {
            console.error("Upload error:", error);
            this.state.error = "Upload failed";
        }
    }

    async onDelete() {
        this.destroy();
        this.state.videoUrl = null;
        return this.props.record.update({ 
            [this.props.name]: false, 
            [this.props.filenameField]: false 
        });
    }

    async retry() {
        this.state.error = null;
        this.state.loading = true;
        await this.initContent();
    }
}

export const videoContentField = {
    component: VideoContentField,
    supportedTypes: ["binary"],
    extractProps: ({ attrs }) => ({
        filenameField: attrs.filename,
    }),
};

registry.category("fields").add("video_content", videoContentField);