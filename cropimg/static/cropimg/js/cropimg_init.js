void(function() {

    function on_file_change(thumbnail_data) {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            var thumbnail = $(thumbnail_data.thumbnail_image_id);
            thumbnail.attr('src', '');
            if (thumbnail.data("cropimg")) {
                var cropimg = thumbnail.data("cropimg");
                cropimg.reset();
                //The plugin doesn't get totally destroyed so I delete it manually and remove it from window.resize event
                cropimg = cropimg.main;
                for (var prop in cropimg) {
                    if (cropimg.hasOwnProperty(prop)) {delete cropimg[prop]}
                }
                $(window).off("resize");
            }
            $("#" + thumbnail_data.my_id).val("");
            reader.onload = function (e) {
                thumbnail = $(thumbnail_data.thumbnail_image_id);
                set_thumbnail(thumbnail, e.target.result, thumbnail_data);
            }.bind(this);

            reader.readAsDataURL(this.files[0]);
        }
    }

    function set_thumbnail(thumbnail, src, thumbnail_data) {
        if (src) {
            thumbnail.attr("src", src);
            thumbnail.cropimg(thumbnail_data.cropimg_args);
        }
    }

    function onCroppingSelectionChanged(x, y, width, height) {
        //Invalid data, skip
        if (width <= 0 || height <= 0) return;
        var data = this;
        var input = $("#" + data.my_id);
        x *= -1;
        y *= -1;
        input.val(x + "," + y + "," + width + "," + height);
    }

    function setImgCropData(imgcrop, x, y, w) {
        var main = imgcrop.main;
        w = w || main.imageData.originalWidth;
        var ratio = main.imageContainer.width() / w;
        x = Math.round(x * ratio * -1);
        y = Math.round(y * ratio * -1);

        main.imageData.proportions = ratio;
        main.Zooming.eventMouseClick("out");
        main.Zooming.eventMouseClick("in");
        main.CroppingResult.update(x, y);
        main.image.css({"left": x, "top": y});
    }

    function onImgCropInit() {
        var data = this;
        var $field = $("#" + data.my_id);
        var thumbnail_image = $(data.thumbnail_image_id);
        //If the field is not empty, update the cropimg to match its values
        var x;
        var y;
        var w;
        var cropimg = thumbnail_image.data("cropimg");
        if ($field.val()) {
            var vallist = $field.val().split(",");
            x = parseInt(vallist[0]);
            y = parseInt(vallist[1]);
            w = parseInt(vallist[2]);
        } else { // No data set, default to whole image
            x = y = 0;
            w = 0;
        }
        setImgCropData(cropimg, x, y, w);
    }

    window.initialize_cropimg_fields = function() {
        var thumbnail_fields = $("input[data-type=thumbnail_field]");
        thumbnail_fields.each(function (_, my_field) {
            $field = $(my_field);
            //If field already initialized, move on
            if ($field.data("thumbnail-data")) return;

            var thumb_size = $field.attr("data-thumb-size").split(",").map(function(x) {return parseInt(x)});
            var data = {};
            data.my_name = $field.attr("data-thumb-field") || $field.attr("name");
            data.my_id = $field.attr("id");
            data.cropimg_args = {
                resultWidth: thumb_size[0], resultHeight: thumb_size[1],
                displayFixingPositionsButtons: thumb_size[0] > 100,
                maxContainerWidth: 400, inputPrefix: "ci-" + data.my_id,
                onChange: onCroppingSelectionChanged.bind(data),
                onInit: onImgCropInit.bind(data)
            };
            //Thumbnail names should be based on field name to avoid conflict in case of formsets
            data.image_field_id = "#" + data.my_id.replace(data.my_name, $field.attr("data-image-field"));
            var image_field = $(data.image_field_id);
            var image_value = image_field.attr("data-value");
            data.thumbnail_image_id = "#" + data.my_id + "-img";
            var thumbnail_image = $(data.thumbnail_image_id);
            $field.data("thumbnail-data", data);
            image_field.change($.proxy(on_file_change, image_field[0], data));
            set_thumbnail(thumbnail_image, image_value, data);
        });
    };

    //When initializing cropimg then reinitialize it again (for example when your form is part of dynamically loaded content),
    //bugs starts to appear related to image size, adding 200 millisec delay seems to solve the problem
    jQuery(function() {setTimeout(window.initialize_cropimg_fields, 200)});
}());

