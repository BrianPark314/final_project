var Camera = {

    data: vm => ({
        width: 320,    // Photo scales width to this
        height: 0,     // Computed based on the input stream
        streaming: false,
        video: null,
        canvas: null,
        startbutton: null,
        preview: false,
        saved: false,
        data: "",
        css: {
            video:
                `
                    border: 1px solid black;
                    box-shadow: 2px 2px 3px black;
                    width:320px;
                    height:240px;
                `,
            startbutton:
                `
                display:block;
                position:relative;
                margin-left:auto;
                margin-right:auto;
                bottom:32px;
                background-color: rgba(0, 150, 0, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.7);
                box-shadow: 0px 0px 1px 2px rgba(0, 0, 0, 0.2);
                font-size: 14px;
                font-family: "Lucida Grande", "Arial", sans-serif;
                color: rgba(255, 255, 255, 1.0);
              
            `,
            camera:
                `
                width: 340px;
                display:inline-block;
            `,
            previewButtonPanel:
                `
            width: 60%;
            display:block;
            position:relative;
            margin-left:auto;
            margin-right:auto;
            bottom:32px;
            `,
            previewButton:
                `
            display:inline;
            position:relative;
            background-color: rgba(0, 150, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.7);
            box-shadow: 0px 0px 1px 2px rgba(0, 0, 0, 0.2);
            font-size: 14px;
            font-family: "Lucida Grande", "Arial", sans-serif;
            color: rgba(255, 255, 255, 1.0);
          
            `
        }
    }),

    watch: {

    },

    mounted: function () {

        this.root = this.$el;
        console.log('Mounted', this.root.children[0].children[0])

        this.video = this.root.children[0].children[0].children[0];
        this.startbutton = this.root.children[0].children[0].children[1];

        this.canvas = this.root.children[0].children[1].children[0];

        this.startup()
    },

    methods: {
        cancelClick: function () {
            console.log('Cancel fired')
            this.preview = false
        },

        save: function () {
            this.$emit('photo-clicked', { 'imageData': this.data.substring("data:image/png;base64,".length), 'type': 'image/png' })
            this.saved = true
        },

        startup: function () {

            navigator.mediaDevices.getUserMedia({ video: true, audio: false })
                .then((stream) => {
                    this.video.srcObject = stream;
                    this.video.play();
                })
                .catch((err) => {
                    console.log("An error occurred: " + err);
                });

            this.video.addEventListener('canplay', (ev) => {
                if (!this.streaming) {
                    this.height = this.video.videoHeight / (this.video.videoWidth / this.width);

                    // Firefox currently has a bug where the height can't be read from
                    // the video, so we will make assumptions if this happens.

                    if (isNaN(this.height)) {
                        this.height = this.width / (4 / 3);
                    }

                    this.video.setAttribute('width', this.width);
                    this.video.setAttribute('height', this.height);
                    this.canvas.setAttribute('width', this.width);
                    this.canvas.setAttribute('height', this.height);
                    this.streaming = true;
                }
            }, false);
            this.startbutton.addEventListener('click', (ev) => {
                this.takepicture();
                ev.preventDefault();
            }, false);

            this.clearphoto();
        },

        // Fill the photo with an indication that none has been
        // captured.

        clearphoto: function () {
            var context = this.canvas.getContext('2d');
            context.fillStyle = "#AAA";
            context.fillRect(0, 0, this.canvas.width, this.canvas.height);

            this.data = this.canvas.toDataURL('image/png');

        },

        // Capture a photo by fetching the current contents of the video
        // and drawing it into a canvas, then converting that to a PNG
        // format data URL. By drawing it on an offscreen canvas and then
        // drawing that to the screen, we can change its size and/or apply
        // other changes before drawing it.

        takepicture: function () {
            var context = this.canvas.getContext('2d');
            if (this.width && this.height) {
                this.canvas.width = this.width;
                this.canvas.height = this.height;
                context.drawImage(this.video, 0, 0, this.width, this.height);

                this.data = this.canvas.toDataURL('image/png');
                this.preview = true
                this.saved = false

            } else {
                this.clearphoto();
            }
        }
    },
    template:
        `
        <v-container>
            <div class="contentarea">
                <div v-bind:style="css.camera" v-show="!preview">
                    <video v-bind:style="css.video">Video stream not available.</video>
                    <button v-bind:style="css.startbutton">Take photo</button>
                </div>
                <div v-bind:style="css.camera" v-show="preview">
                    <canvas>
                    </canvas>
                    <span v-bind:style="css.previewButtonPanel">
                        <button v-bind:style="css.previewButton" v-on:click="cancelClick">Click Again</button>
                        <button v-bind:style="css.previewButton" v-show="!saved" v-on:click="save">Save</button>
                    </span>
                </div>
            </div>
        </v-container>
    `
}

