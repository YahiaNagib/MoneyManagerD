
window.onload = function() {

    const expense = 1;
    const income = 2;
    
    CallAjax(expense) // to call for expenses items from the server, 1 means expenses (default)
    
    function CallAjax(categoryTypeId) {
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
        $.ajax({
            url: "/statistics/",
            data: {
                'CategoryType': categoryTypeId       // add the category id to the GET parameters
            },
            'type': 'POST',
            success: function (items) {   // `items` is the return of the `load_categories` view function
            var chart = new CanvasJS.Chart("chartContainer",
            {
                backgroundColor: "transparent",
                title: {
                    text: ""
                },
                legend: {
                    maxWidth: 350,
                    itemWidth: 120,
                    horizontalAlign: "right",
                    verticalAlign: "center"
                },
                data: [
                    {
                        type: "pie",
                        showInLegend: true,
                        legendText: "{indexLabel}",
                        dataPoints: items,
                    }
                ]
                    });
                    chart.render();  // replace the contents of the category input with the data that came from the server
                }
        });
    }
    // Copied from Django Documentaion
    // Used to add csrf token the the form
    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    }
    $(".expense_btn").click(function () {
        CallAjax(expense)
        $(".expense_btn").css("background-color", "#007bff")
        $(".expense_btn").css("color", "#fff")
        $(".income_btn").css("background-color", "transparent")
        $(".income_btn").css("color", "#007bff")
        $(".expenses-list").css("display", "block")
        $(".income-list").css("display", "none")
        $(".category_input").attr("name", "new_expense")
    }
    )
    $(".income_btn").click(function () {
        CallAjax(income)
        $(".expense_btn").css("background-color", "transparent")
        $(".expense_btn").css("color", "#007bff")
        $(".income_btn").css("background-color", "#007bff")
        $(".income_btn").css("color", "#fff")
        $(".expenses-list").css("display", "none")
        $(".income-list").css("display", "block")
        $(".category_input").attr("name", "new_income")
    }
    )
    
}
