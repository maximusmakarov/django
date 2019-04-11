window.onload = function () {
    $('.basket-list').on('change', 'input[type="number"]', function (event) {
        let targetHref = event.target;

        $.ajax({
            url: "/basket/update/" + targetHref.name + "/" + targetHref.value + "/",
            success: function (data) {
                $('.basket-list').html(data.result);
            }
        });

        event.preventDefault();
    });
}
