"use strict";

window.onload = function () {
    let _quantity, _price, orderitemNum, deltaQuantity, orderitemQuantity, deltaCost;
    let quantityArr = [];
    let priceArr = [];

    let totalForms = parseInt($(`input[name="orderitems-TOTAL_FORMS"]`).val());
    let $orderTotalCost = $(`.order_total_cost`);
    let $orderTotalQuantity = $(`.order_total_quantity`);

    let orderTotalQuantity = parseInt($orderTotalQuantity.text()) || 0;
    let orderTotalCost = parseFloat($orderTotalCost.text().replace('.', ',')) || 0;
    let $orderForm = $(`.order_form`);

    for (let i=0; i < totalForms; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace('.', ','));
        quantityArr[i] = _quantity;
        priceArr[i] = _price ? _price: 0    ;
    }

    if (!orderTotalQuantity) {
        orderSummaryRecalc();
    }

    function orderSummaryRecalc() {
        orderTotalQuantity = 0;
        orderTotalCost = 0;

        for (let i=0; i < totalForms; i++) {
            orderTotalQuantity += quantityArr[i];
            orderTotalCost += quantityArr[i] * priceArr[i];
        }
        $(`.order_total_quantity`).html(orderTotalQuantity.toString());
        $(`.order_total_cost`).html(Number(orderTotalCost).toFixed(2).replace('.', ','));
    }

    function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
        deltaCost = orderitemPrice * deltaQuantity;

        orderTotalCost = (orderTotalCost + deltaCost);
        orderTotalQuantity = orderTotalQuantity + deltaQuantity;

        $(`.order_total_quantity`).html(orderTotalQuantity.toString());
        $(`.order_total_cost`).html(Number(orderTotalCost).toFixed(2).replace('.', ','));
    }

    function deleteOrderItem(row) {
        let targetName= row[0].querySelector('input[type="number"]').name;
        let orderitemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
        let deltaQuantity = -quantityArr[orderitemNum];
        quantityArr[orderitemNum] = 0;
        if (!isNaN(priceArr[orderitemNum]) && !isNaN(deltaQuantity)) {
            orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
        }

        orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
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

    $(`.formset_row`).formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    $orderForm.on('change', 'select', function (event) {
        let target = event.target;
        orderitemNum = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        let orderitemProductPK = target.value;

        if (orderitemProductPK) {
            $.ajax({
                url: "/orders/product/" + orderitemProductPK + "/price/",
                success: function (data) {
                    if (data.price) {
                        priceArr[orderitemNum] = parseFloat(data.price);
                        if (isNaN(quantityArr[orderitemNum])) {
                            quantityArr[orderitemNum] = 0;
                        }
                        let priceHtml = '<span>' + data.price.toString().replace('.', ',') + '</span> руб';
                        let currentTr = $('.order_form table').find('tr:eq(' + (orderitemNum + 1) + ')');


                        currentTr.find('td:eq(2)').html(priceHtml);

                        if (isNaN(currentTr.find('input[type="number"]').val())) {
                            currentTr.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalc();
                    }
                },
            });
        }


    });




};