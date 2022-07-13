function reset_table(){
    $("#demo-table").html("<table id=\"demo-table\"></table>")
    $('#demo-table tr:last').after('<tr><td>File Name</td><td>File path</td><td>Size</td></tr>');
};

$("#submit").click(function() {
    $.post( "demo/home_p/", { filename: $("#search_name").val() }, function(data) {
        reset_table();
        for (result in data.resultData) {
            $('#demo-table tr:last').after('<tr><td>'+result.name+'</td><td>'+result.path+'</td><td>'+result.path+'</td></tr>');
        }
        $("#table-div").show();
    }, "json");
});