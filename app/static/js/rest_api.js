$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_category").val(res.category);
        $("#product_price").val(parseFloat(res.price).toFixed(2));
        if (res.available == true) {
            $("#product_available").val("true");
        } else {
            $("#product_available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_category").val("");
        $("#product_price").val("");
        $("#product_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a product
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var price = $("#product_price").val();
        var available = $("#product_available").val() == "true";

        var data = {
            "name": name,
            "category": category,
            "available": available,
            "price": price,
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/products",
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
    // Update a product
    // ****************************************

    $("#update-btn").click(function () {

        var product_id = $("#product_id").val();
        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var price = $("#product_price").val();
        var available = $("#product_available").val() == "true";

        var data = {
            "name": name,
            "category": category,
            "price": price,
            "available": available
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/products/" + product_id,
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
    // Retrieve a product
    // ****************************************

    $("#retrieve-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/products/" + product_id,
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
    // Delete a product
    // ****************************************

    $("#delete-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/products/" + product_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product with ID [" + res.id + "] has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a product
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var price = $("#product_price").val();
        var available = $("#product_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }
        if (price) {
            if (queryString.length > 0) {
                queryString += '&price=' + price
            } else {
                queryString += 'price=' + price
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/products?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:40%">Price</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                var product = res[i];
                var row = "<tr><td>" +
                    product.id + "</td><td>" +
                    product.name + "</td><td>" +
                    product.category + "</td><td>" + 
                    product.price + "</td><td>" +
                    product.available + "</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // List all products
    // ****************************************
    $("#listAll-btn").click(function() {
        var ajax = $.ajax({
            type: "GET",
            url: "/products",
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res) {
            $("#search_results").empty();
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>';
            header += '<th style="width:20%">Name</th>';
            header += '<th style="width:13%">Category</th>';
            header += '<th style="width:10%">Price</th>';
            header += '<th style="width:10%">Available</th></tr>';
            $("#search_results").append(header);
            for (var i = 0; i < res.length; i++) {
                var product = res[i];
                var row = "<tr><td>" +
                    product.id + "</td><td>" +
                    product.name + "</td><td>" +
                    product.category + "</td><td>" + 
                    product.price + "</td><td>" +
                    product.available + "</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success");
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message);
        });
    });

})
