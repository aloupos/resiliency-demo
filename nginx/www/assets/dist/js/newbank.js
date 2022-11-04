
function fillBalances (bdata) {
    $("#acct_name").text(bdata[0].product_name);
    $("#acct_balance").text('$' + Number(bdata[0].balance).toLocaleString('en'));
    $("#acct2_name").text(bdata[1].product_name);
    $("#acct2_balance").text('$' + Number(bdata[1].balance).toLocaleString('en'));
}
$("button").click(function(e){
    var btnid = e.target.id;
    url = 'http://52.116.206.161:5000/transactions'
    if (btnid == 'transactions1') {
      params = {account_id: 1}
    }
    else {
      params = {account_id: 2}
    }
    $.getJSON(url , params, function(data) {
    var div = document.createElement("div");
    // <div class="col-md-12" id="viewpane">
    div.className = "col-md-12";
    div.id = "viewpane";
    var tbl = document.createElement("table");
    //var tbl = div.createElement ("table");
    tbl.className = "table table-striped table-hover"
    var tbl_body = tbl.createTBody();

    var tbl_head = tbl.createTHead();

    tbl_head_row = tbl_head.insertRow()
    tbl_head_row.insertCell().appendChild(document.createTextNode('Date'))
    tbl_head_row.insertCell().appendChild(document.createTextNode('Merchant'))
    tbl_head_row.insertCell().appendChild(document.createTextNode('Description'))
    tbl_head_row.insertCell().appendChild(document.createTextNode('Credit'))
    tbl_head_row.insertCell().appendChild(document.createTextNode('Debit'))

    var odd_even = false;
    $.each(data, function() {

        var tbl_row = tbl_body.insertRow();
        tbl_row.insertCell().appendChild(document.createTextNode(this.date.toString()));
        tbl_row.insertCell().appendChild(document.createTextNode(this.merchant.toString()));
        tbl_row.insertCell().appendChild(document.createTextNode(this.description.toString()));
        tbl_row.insertCell().appendChild(document.createTextNode(this.credit_amount.toString()));
        tbl_row.insertCell().appendChild(document.createTextNode(this.debit_amount.toString()));
        tbl_row.className = odd_even ? "odd" : "even";
        odd_even = !odd_even;
    });
    div.innerHTML=(tbl.outerHTML)
    console.log (tbl.innerHTML)
    console.log (tbl.outerHTML)
    $("#viewpane").replaceWith(div);
});
});

$( document ).ready(function() {
    console.log( "ready!" );
  $.ajax({
  url: 'http://52.116.206.161:5000/balance',
  type: "GET",
  dataType: "json",
  complete: function (data_response) {

    //console.log (data_response.responseJSON[0]);
    fillBalances (data_response.responseJSON)
  },
  success: function (data) {
    //console.log ("**");
  }
  });
});
