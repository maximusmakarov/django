window.onload = function () {
    $('.basket_list').change( 'input[type="number"]',function (event) {

        let targetHref = event.target;

        $.ajax({
            url: "/basket/update/" + targetHref.name + "/" + targetHref.value + "/",
            success: function (data) {
                $('.basket_list').html(data.result);
            }
        });

        event.preventDefault();
    });
};
