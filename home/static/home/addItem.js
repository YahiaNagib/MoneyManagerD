$(document).ready(function () {
    var today = new Date();
    $('.date_field').val(today.toISOString().substr(0, 10));

    $(".category_type_list").change(function () {
        var url = $("#ItemForm").attr("category-url");  // get the url of the `load_categories` view
        var categoryTypeId = $(this).val();  // get the selected category ID from the HTML input

        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-categories/)
            data: {
                'CategoryType': categoryTypeId       // add the category id to the GET parameters
            },
            success: function (data) {   // `data` is the return of the `load_categories` view function
                $(".category_types").html(data);  // replace the contents of the category input with the data that came from the server
            }
        });

    });
});