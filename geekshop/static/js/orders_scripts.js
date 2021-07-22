window.onload = function (){
    let _quantity, _price, _orderitemNum, deltaQuantity, orderItemQuantity, deltaCost;
    let quantityArr = [];
    let priceArr =[];
    let totalForms =parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
    let orderTotalQuantity = parseInt($('.order_total_quantity').text()) || 0;
    let orderTotalCost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
    for (var i=0; i < totalForms; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i +'-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantityArr[i] = _quantity;
        if (_price) {
            priceArr[i] = _price;
        } else {
           priceArr[i] = 0;
        }
    }
    $('.order_form').on('click', 'input[type="number"]', function() {
    let target = event.target;
    _orderitemNum = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
    if (priceArr[_orderitemNum]) {
       orderItemQuantity = parseInt(target.value);
       deltaQuantity = orderItemQuantity - quantityArr[_orderitemNum];
       quantityArr[_orderitemNum] = orderItemQuantity;
       orderSummaryUpdate(priceArr[_orderitemNum], deltaQuantity);
        }
    })

    $('.order_form').on('click', 'input[type="checkbox"]', function() {
    let target = event.target;
    _orderitemNum = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
    if(target.checked){
        deltaQuantity = -quantityArr[_orderitemNum]}
    else{
        deltaQuantity = +quantityArr[_orderitemNum]}
    orderSummaryUpdate(priceArr[_orderitemNum], deltaQuantity);
    });
    function orderSummaryRecalc();

    function orderSummaryRecalc(){
        orderTotalCost = 0
        orderTotalQuantity = 0

        for(let i=0; i<totalForms; i++){
            orderTotalCost += priceArr[i]*quantityArr[i]
            orderTotalQuantity += quantityArr[i]
        $('.order_total_cost').html(orderTotalCost.toString());
        $('.order_total_quantity').html(orderTotalQuantity.toString());

        }
    }

    function orderSummaryUpdate(orderItemPrice, deltaQuantity){
        deltaCost = orderItemPrice * deltaQuantity;
        orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
        orderTotalQuantity = orderTotalQuantity + deltaQuantity;
        // console.log(orderTotalCost, orderTotalQuantity )
        $('.order_total_cost').html(orderTotalCost.toString());
        $('.order_total_quantity').html(orderTotalQuantity.toString());
    }

    $('.formset_row').formset({
    addText: 'добавить продукт',
    deleteText: 'удалить',
    prefix: 'orderitems',
    removed: deleteOrderItem
    });

    function deleteOrderItem(row) {
    let targetName= row[0].querySelector('input[type="number"]').name;
    _orderitemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
    deltaQuantity= -quantityArr[_orderitemNum];
    orderSummaryUpdate(priceArr[_orderitemNum], deltaQuantity);
    }

     $('.order_form select').change(function() {
         target = event.target
         _orderitemNum = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
         let orderItemProductPk = target.options[target.selectedIndex].value;
         // console.log(orderItemProductPk)
         if (orderItemProductPk) {
             $.ajax({
                 url: "/order/product/" + orderItemProductPk + "/price/",
                 success: function (data) {
                     if (data.price) {
                         priceArr[_orderitemNum] = parseFloat(data.price)
                         if (isNaN(quantityArr[_orderitemNum])) {
                             quantityArr[_orderitemNum] = 0
                         }
                         let priceHtml = "<span className='orderitems-" + _orderitemNum + "-price'>" + data.price.toString().replace('.', ',') + "</span>"
                         let currentTr = $('.order_form table').find('tr:eq(' + (_orderitemNum + 1) + ')')
                         // console.log(currentTr.find('td:eq(2)'))
                         currentTr.find('td:eq(2)').html(priceHtml);
                         orderSummaryRecalc();

                     }
                 }

             });

         }
     })
}