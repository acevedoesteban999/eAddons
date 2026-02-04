/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState, onMounted, onWillUpdateProps, onWillUnmount, useRef } from "@odoo/owl";
import { FileUploader } from "@web/views/fields/file_handler";
import { loadJS, loadCSS } from "@web/core/assets";

const MAX_INLINE_SIZE = 2 * 1024 * 1024; // 2MB

export class VideoContentField extends Component {
    static template = "e_video_content.VideoContentField";
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
            isNewUpload: false,
        });
        this.player = null;
        this.playerRef = useRef("player");
        this.uploadedData = null;
        this.objectUrl = null;
        
        onMounted(() => this.init());
        
        onWillUpdateProps((nextProps) => {
            const currentData = this.props.record.data[this.props.name];
            const nextData = nextProps.record.data[this.props.name];
            
            if (this.state.isNewUpload && nextData && nextData !== currentData) {
                this.state.isNewUpload = false;
                this.uploadedData = null;
                setTimeout(() => this.init(), 100);
            }
        });
        
        onWillUnmount(() => this.destroy());
    }

    async init() {
        const recordId = this.props.record.resId;
        const resModel = this.props.record.resModel; // Obtiene el modelo dinámicamente
        const fieldValue = this.props.record.data[this.props.name];
        
        this.state.error = null;
        this.cleanupObjectUrl();
        
        if (!recordId || !fieldValue) {
            this.state.videoUrl = null;
            this.destroyPlayer();
            return;
        }

        this.state.loading = true;

        try {
            // Detecta base64 (upload nuevo)
            if (typeof fieldValue === 'string' && fieldValue.length > 1000) {
                this.state.isNewUpload = true;
                this.uploadedData = fieldValue;
                
                if (fieldValue.length < MAX_INLINE_SIZE * 1.4) {
                    const blob = this.base64ToBlob(fieldValue);
                    this.objectUrl = URL.createObjectURL(blob);
                    this.state.videoUrl = this.objectUrl;
                } else {
                    this.state.videoUrl = null;
                    this.state.error = "Video uploading... Please save the record.";
                }
                
                await this.loadPlyr();
                await this.initPlayer();
                return;
            }

            // Record guardado - streaming con modelo dinámico
            this.state.isNewUpload = false;
            this.state.videoUrl = `/e_video_content/video/stream/${resModel}/${recordId}`;
            
            await this.loadPlyr();
            await this.initPlayer();
            
        } catch (error) {
            console.error("VideoContent init error:", error);
            this.state.error = "Failed to load video player";
        } finally {
            this.state.loading = false;
        }
    }

    base64ToBlob(base64) {
        const byteString = atob(base64);
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: 'video/mp4' });
    }

    async loadPlyr() {
        if (window.Plyr && this.state.libsLoaded) return;
        await Promise.all([
            loadCSS("/e_video_content/static/src/library/plyr/plyr.css"),
            loadJS("/e_video_content/static/src/library/plyr/plyr.js"),
        ]);
        this.state.libsLoaded = true;
    }

    async initPlayer() {
        if (!this.playerRef.el || !window.Plyr) return;

        this.destroyPlayer();

        this.player = new Plyr(this.playerRef.el, {
            controls: [
                'play-large', 'play', 'progress', 'current-time', 'duration',
                'mute', 'volume', 'captions', 'settings', 'pip', 'airplay', 'fullscreen'
            ],
            settings: ['captions', 'quality', 'speed', 'loop'],
            loadSprite: true,
            iconUrl: null,
            blankVideo: null,
            autoplay: false,
            preload: 'metadata',
            storage: { enabled: false },
            tooltips: { controls: true, seek: true },
            quality: {
                default: 1080,
                options: [4320, 2880, 2160, 1440, 1080, 720, 576, 480, 360, 240],
            },
            speed: {
                selected: 1,
                options: [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
            },
            keyboard: { focused: true, global: false },
            clickToPlay: true,
            hideControls: true,
            resetOnEnd: false,
            buffered: true,
            debug: false,
        });

        this.player.on('ready', () => {
            this.state.loading = false;
        });

        this.player.on('error', () => {
            this.state.error = "Video playback error";
            this.state.loading = false;
        });

        this.player.on('loadedmetadata', () => {
            this.state.loading = false;
        });
    }

    destroyPlayer() {
        if (this.player) {
            try {
                this.player.destroy();
            } catch (e) {
                console.warn("Error destroying player:", e);
            }
            this.player = null;
        }
    }

    cleanupObjectUrl() {
        if (this.objectUrl) {
            URL.revokeObjectURL(this.objectUrl);
            this.objectUrl = null;
        }
    }

    destroy() {
        this.destroyPlayer();
        this.cleanupObjectUrl();
    }

    get hasVideo() {
        return !!this.state.videoUrl;
    }

    get filename() {
        return this.props.record.data[this.props.filenameField] || "video.mp4";
    }

    async update({ data, name }) {
        this.destroyPlayer();
        this.cleanupObjectUrl();
        
        if (!data) {
            this.state.videoUrl = null;
            this.state.isNewUpload = false;
            this.uploadedData = null;
            return this.props.record.update({ 
                [this.props.name]: false,
                [this.props.filenameField]: false 
            });
        }

        this.state.isNewUpload = true;
        this.uploadedData = data;
        
        try {
            await this.props.record.update({ 
                [this.props.name]: data, 
                [this.props.filenameField]: name 
            });
            
            this.init();    
            
        } catch (error) {
            console.error("Upload error:", error);
            this.state.error = "Upload failed";
        }
    }

    async onDelete() {
        this.destroy();
        this.state.videoUrl = null;
        this.state.isNewUpload = false;
        this.uploadedData = null;
        return this.props.record.update({ 
            [this.props.name]: false, 
            [this.props.filenameField]: false 
        });
    }

    async retry() {
        this.state.error = null;
        await this.init();
    }
}

export const videoContentField = {
    component: VideoContentField,
    supportedTypes: ["binary"],
    extractProps: ({ attrs }) => ({ filenameField: attrs.filename }),
};

registry.category("fields").add("video_content", videoContentField);