window.onload = function () {
    let _quantity, _price, orderitemNum, deltaQuantity, orderitemQuantity, deltaCost;
    let quantityArr = [];
    let priceArr = [];

    let totalForms = parseInt($(`input[name="orderitems-TOTAL_FORMS"]`).val());
    let $orderTotalCost = $(`.order_total_cost`);
    let $orderTotalQuantity = $(`.order_total_quantity`);

    let orderTotalQuantity = parseInt($orderTotalQuantity.text()) || 0;
    let orderTotalCost = parseFloat($orderTotalCost.text().replace(',', '.')) || 0;
    let $orderForm = $(`.order_form`);

    for (let i=0; i < totalForms; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantityArr[i] = _quantity;
        priceArr[i] = _price ? _price: 0    ;
    }

    function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
        deltaCost = orderitemPrice * deltaQuantity;

        orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
        orderTotalQuantity = orderTotalQuantity + deltaQuantity;

        $orderTotalCost.html(orderTotalCost.toString());
        $orderTotalQuantity.html(orderTotalQuantity.toString());
    }

    if (!orderTotalQuantity) {
        for (let i=0; i < totalForms; i++) {
            orderTotalQuantity += quantityArr[i];
            orderTotalCost += quantityArr[i] * priceArr[i];
        }
        $orderTotalQuantity.html(orderTotalQuantity.toString());
        $orderTotalCost.html(Number(orderTotalCost.toFixed(2)).toString());
    }

    $orderForm.on('change', 'input[type="number"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (priceArr[orderitemNum]) {
            orderitemQuantity = parseInt(event.target.value);
            deltaQuantity = orderitemQuantity - quantityArr[orderitemNum];
            quantityArr[orderitemNum] = orderitemQuantity;
            orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
        }
    });

    $orderForm.on('change', 'input[type="checkbox"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (event.target.checked) {
            deltaQuantity = -quantityArr[orderitemNum];
        } else {
            deltaQuantity = quantityArr[orderitemNum];
        }
        orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
    });


};