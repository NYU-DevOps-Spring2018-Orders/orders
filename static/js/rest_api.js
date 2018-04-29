$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#order_customer_id").val(res.customer_id);
        var myDate = new Date(res.date);
        var date = myDate.toISOString();
        date = date.slice(0, -8);
        $("#order_date").val(date);
        $("#order_status").val(res.status);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#order_customer_id").val("");
        $("#order_date").val("");
        $("#order_status").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    /// Clears all form fields
    function clear_item_form_data() {
        $("#item_product_id").val("");
        $("#item_order_id").val("");
        $("#item_name").val("");
        $("#item_quantity").val("");
        $("#item_price").val("");
    }

    // Updates the form with data from the response
    function update_item_form_data(res) {
        $("#item_order_id").val(res.order_id);
        $("#item_product_id").val(res.product_id);
        $("#item_name").val(res.name);
        $("#item_quantity").val(res.quantity);
        $("#item_price").val(res.price);
    }

    // add items to orders
    var items_for_order = [];

    function update_items_view() {
        $("#items_for_order").empty();
        $("#items_for_order").append('<table class="table-striped">');
        var header = '<tr>'
        header += '<th style="width:10%">Product ID</th>'
        header += '<th style="width:40%">Name</th>'
        header += '<th style="width:25%">Quantity</th>'
        header += '<th style="width:25%">Price</th></tr>'
        $("#items_for_order").append(header);
        for(var i = 0; i < items_for_order.length; i++) {
            item = items_for_order[i];
            var row = "<tr><td>"+item.product_id+"</td><td>"+item.name+"</td><td>"+item.quantity+"</td><td>"+item.price+"</td></tr>";
            $("#items_for_order").append(row);
        }

        $("#items_for_order").append('</table>');
    }

    // ****************************************
    // Create an Order
    // ****************************************

    $("#create-btn").click(function () {

        var customer_id = $("#order_customer_id").val();
        var date = $("#order_date").val();
        var status = $("#order_status").val();
        var items = items_for_order;

        var data = {
            "customer_id": customer_id,
            "date": date,
            "status": status,
            "items": items
        };

        console.log(JSON.stringify(data));

        var ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Order
    // ****************************************

    $("#update-btn").click(function () {

        var order_id = $("#order_id").val();
        var customer_id = $("#order_customer_id").val();
        var date = $("#order_date").val();
        var status = $("#order_status").val();
        var items = items_for_order;

        var data = {
            "customer_id": customer_id,
            "date": date,
            "status": status,
            "items": items
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/orders/" + order_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        var order_id = $("#order_id").val();
        var ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Order
    // ****************************************

    $("#delete-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Order has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data()
    });

    // ****************************************
    // View Orders
    // ****************************************

    $("#list-btn").click(function () {

        var ajax = $.ajax({
            type: "GET",
            url: "/orders",
            contentType:"application/json"
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#order_results").empty();
            $("#order_results").append('Orders:');
            $("#order_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Customer ID</th>'
            header += '<th style="width:40%">Date</th>'
            header += '<th style="width:10%">Status</th></tr>'
            $("#order_results").append(header);
            for(var i = 0; i < res.length; i++) {
                order = res[i];
                var row = "<tr><td>"+order.id+"</td><td>"+order.customer_id+"</td><td>"+order.date+"</td><td>"+order.status+"</td></tr>";
                $("#order_results").append(row);
            }

            $("#order_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-btn-item").click(function () {

        var product_id = $("#item_product_id").val();
        var name = $("#item_name").val();
        var quantity = $("#item_quantity").val();
        var price = $("#item_price").val();;

        var data = {
            "product_id": product_id,
            "name": name,
            "quantity": quantity,
            "price": price
        };

        items_for_order.push(data);
        console.log(data);

        clear_item_form_data();

        update_items_view();

    });


    // ****************************************
    // Update an Item
    // ****************************************

    $("#update-btn-item").click(function () {

        var item_id = $("#item_id").val();
        var order_id = $("#item_order_id").val();
        var product_id = $("#item_product_id").val();
        var name = $("#item_name").val();
        var quantity = $("#item_quantity").val();
        var price = $("#item_price").val();

        var data = {
            "product_id": product_id,
            "name": name,
            "quantity": quantity,
            "price": price
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/orders/" + order_id + "/items/" + item_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-btn-item").click(function () {

        var item_id = $("#item_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/items/" + item_id,
            contentType:"application/json"
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_item_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-btn-item").click(function () {

        var item_id = $("#item_id").val();
        var order_id = $("#item_order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id + "/items/" + item_id,
            contentType:"application/json"
        })

        ajax.done(function(res){
            clear_item_form_data()
            flash_message("Item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data()
    });

    $("#clear-btn-item").click(function () {
        $("#item_id").val("");
        clear_item_form_data()
    });


    // ****************************************
    // View Items
    // ****************************************

    $("#list-btn-item").click(function () {

        var ajax = $.ajax({
            type: "GET",
            url: "/items",
            contentType:"application/json"
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#item_results").empty();
            $("#item_results").append('Items:');
            $("#item_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:10%">Order ID</th>'
            header += '<th style="width:10%">Product ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:15%">Quantity</th>'
            header += '<th style="width:15%">Price</th></tr>'
            $("#item_results").append(header);
            for(var i = 0; i < res.length; i++) {
                item = res[i];
                var row = "<tr><td>"+item.id+"</td><td>"+item.order_id+"</td><td>"+item.product_id+"</td><td>"+item.name+"</td><td>"+item.quantity+"</td><td>"+item.price+"</td></tr>";
                $("#item_results").append(row);
            }

            $("#item_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
