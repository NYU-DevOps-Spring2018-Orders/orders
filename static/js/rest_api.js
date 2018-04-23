$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#order_customer_id").val(res.customer_id);
        $("#order_date").val(res.order_date);
        $("#order_status").val(res.order_status);
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

    // add items to orders
    var items_for_order = [];
    function add_item(item) {
      items_for_order = items_for_order.append(item)
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
            flash_message("Order with ID [" + res.id + "] has been Deleted!")
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
            $("#order_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Customer ID</th>'
            header += '<th style="width:40%">Date</th>'
            header += '<th style="width:10%">Status</th></tr>'
            $("#order_results").append(header);
            for(var i = 0; i < res.length; i++) {
                order = res[i];
                var row = "<tr><td>"+order.id+"</td><td>"+order.name+"</td><td>"+order.date+"</td><td>"+order.status+"</td></tr>";
                $("#order_results").append(row);
            }

            $("#order_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
