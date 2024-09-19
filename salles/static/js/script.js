function addRow() {
    var table = document.getElementById("table_fruits");

    var row = table.insertRow();

    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    var cell6 = row.insertCell(5);
    

    var name_fruit = document.createElement("input");
    name_fruit.type = "text";
    name_fruit.placeholder = "Nome da Fruta";
    name_fruit.classList.add("fruit-input");
    name_fruit.name = 'fruit_name[]'
    cell1.appendChild(name_fruit);


    cell2.innerHTML = '<span class="classification"></span>';
    cell3.innerHTML = '<span class="fresh_fruits"></span>';


    var quantity_fruit = document.createElement("input");
    quantity_fruit.type = "number";
    quantity_fruit.placeholder = "Quantidade";
    quantity_fruit.classList.add("quantity");
    quantity_fruit.name = 'quantity_number[]';
    cell4.appendChild(quantity_fruit);


    cell5.innerHTML = '<span class="price"></span>';
    cell6.innerHTML = '<span class="total"></span>';


    applyAutocomplete()
}

function applyAutocomplete() {
    $(".fruit-input").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: searchFruitUrl,
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        select: function(event, ui) {
            var input = $(this);
            var row = input.closest("tr");

            row.find(".classification").text(ui.item.classification);
            row.find(".fresh_fruits").text(ui.item.fresh_fruits);
            row.find(".price").text(ui.item.price);
            
        }
    });

    $(".fruit-input").on("input", function() {
        if ($(this).val() === "") {
            $(this).closest("tr").find(".classification").text("");
            $(this).closest("tr").find(".fresh_fruits").text("");
            $(this).closest("tr").find(".price").text("");
        }
    });

    $(document).on("input", ".quantity", function() {
        var quantity = parseFloat($(this).val());
        var price = parseFloat($(this).closest("tr").find(".price").text());  

        if (!isNaN(quantity) && !isNaN(price)) {
            var total = quantity * price;
            $(this).closest("tr").find(".total").text(total.toFixed(2));  
        }

        else {
            $(this).closest("tr").find(".total").text('');
        }
    });
}