
$(".expense_btn").click(function () {
    $(".expense_btn").css("background-color", "#007bff")
    $(".expense_btn").css("color", "#fff")
    $(".income_btn").css("background-color", "transparent")
    $(".income_btn").css("color", "#007bff")
    $(".expense").css("display", "block")
    $(".income").css("display", "none")
    $(".category_input").attr("name", "new_expense")
}
)
$(".income_btn").click(function () {
    $(".expense_btn").css("background-color", "transparent")
    $(".expense_btn").css("color", "#007bff")
    $(".income_btn").css("background-color", "#007bff")
    $(".income_btn").css("color", "#fff")
    $(".expense").css("display", "none")
    $(".income").css("display", "block")
    $(".category_input").attr("name", "new_income")
}
)