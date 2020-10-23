$(document).ready(function(){
    expense_table = jQuery('#expense-list').DataTable({
    "autoWidth": false,
		"language": {
		"emptyTable": "No expanses found"
		 },

    "ajax": {
            // "url": "static/objects2.txt", // This works for the static file
            "url": "/expense_json",
            "dataType": "json",
            "dataSrc": "",
            "contentType":"application/json"
        },
        "aoColumns":[
      { "mData": "id", sDefaultContent : '-', "width": "5%"},
      { "mData": "date", sDefaultContent : '-', "width": "15%"},
      { "mData": "category", sDefaultContent : '-', "width": "7%"},
      { "mData": "amount", sDefaultContent : '-', "width": "20%"},
      { "mData": "paid_to", sDefaultContent : '-', "width": "23%"},
      { "mData": "description", sDefaultContent : '-', "width": "30%"}

    ]

 }
);

    var deleters = $(".delete");
    deleters.on("click", function(){
        // send ajax request to delete this expense
        $.ajax({
            url: `expense/${$(this).attr("data")}/delete`,
            data: {
                "item": "some name",
                "paid_to": "some company"
            },
            success: function(){
                console.log("deleted");
            }
        });        
        // fade out expense
        this_row = $(this.parentNode.parentNode);
        // delete the containing row
        this_row.animate({
            opacity: 0
        }, 500, function(){
            $(this).remove();
        })
    });
});
