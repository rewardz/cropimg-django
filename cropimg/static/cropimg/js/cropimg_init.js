void(function() {

    function on_file_change(thumbnail_data) {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            var thumbnail = $(thumbnail_data.thumbnail_image_id);
            thumbnail.attr('src', '');
            $("#" + thumbnail_data.my_id).val("");
            if (thumbnail.data("cropimg")) {
                thumbnail.data("cropimg").reset();
            }
            reader.onload = function (e) {
                thumbnail = $(thumbnail_data.thumbnail_image_id);
                thumbnail.attr('src', e.target.result);
            }.bind(this);

            reader.readAsDataURL(this.files[0]);
        }
    }

    function on_thumbnail_load(thumbnail_data) {
        var thumbnail = $(this);
        if (thumbnail.attr("src")) {
            thumbnail.cropimg(thumbnail_data.cropimg_args);
        }
    }

    function onCroppingSelectionChanged(x, y, width, height) {
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

        var step = main.options.zoomStep / 1000;
        main.imageData.proportions = ratio + step;
        main.image.css({"left": x, "top": y });
        main.Zooming.eventMouseClick();

        main.CroppingResult.update(x, y,
            main.options.resultWidth * parseFloat(main.CroppingResult.cropPercent),
            main.options.resultHeight * parseFloat(main.CroppingResult.cropPercent),
            true);
    }

    function onImgCropInit() {
        var data = this;
        var $field = $("#" + data.my_id);
        var thumbnail_image = $(data.thumbnail_image_id);
        //If the field is not empty, update the cropimg to match its values
        var x, y, w, h;
        var cropimg = thumbnail_image.data("cropimg");
        if ($field.val()) {
            var vallist = $field.val().split(",");
            x = parseInt(vallist[0]);
            y = parseInt(vallist[1]);
            w = parseInt(vallist[2]);
            setTimeout(setImgCropData, 700, cropimg, x, y, w);
        } else { // No data set, default to whole image
            setTimeout(setImgCropData, 700, cropimg, 0, 0);
        }
    }

    jQuery(function(){
        var thumbnail_fields = $("input[data-type=thumbnail_field]");
        thumbnail_fields.each(function (_, my_field) {
            $field = $(my_field);
            var thumb_size = $field.attr("data-thumb-size").split(",").map(function(x) {return parseInt(x)});
            var data = {};
            data.my_name = $field.attr("data-thumb-field");
            data.my_id = $field.attr("id");
            data.cropimg_args = {
                resultWidth: thumb_size[0], resultHeight: thumb_size[1],
                displayFixingPositionsButtons: thumb_size[0] > 100,
                maxContainerWidth: 400, inputPrefix: "ci-" + data.my_id,
                onChange: onCroppingSelectionChanged.bind(data),
                onInit: onImgCropInit.bind(data)
            };
            data.image_field_id = "#" + data.my_id.replace(data.my_name, $field.attr("data-image-field"));
            var image_field = $(data.image_field_id);
            var image_value = image_field.attr("data-value");
            data.thumbnail_image_id = "#" + data.my_id + "-img";
            var thumbnail_image = $(data.thumbnail_image_id);
            $field.data("thumbnail-data", data);
            image_field.change($.proxy(on_file_change, image_field[0], data));
            thumbnail_image.load($.proxy(on_thumbnail_load, thumbnail_image[0], data));
            thumbnail_image.attr("src", image_value);
        });
    });
}());

