/**
 * Created by User on 08/03/2017.
 */

$("#orderInput").click(function() {
   window.location = "http://127.0.0.1:8000/workorders/order_input";
});


$('#add_part').click(function() {

 /*var structure = $('<hr><div id = "part_order"><div class="row"><div class="col-md-2"><label><b>Quantity</b></label></div>' +
     '<div class="col-md-5"><input class="form-control" type="text" name="Quantity" size="30" placeholder="Quantity...">' +
    '</div></div><br><div class="row"><div class="col-md-2"><label><b>Part</b></label></div><div class="col-md-5">' +
    '<input class="form-control" type="text" name="Quantity" size="30" placeholder="Part..."></div></div><br><div class="row"> ' +
    '<div class="col-md-2"><label><b>Measure</b></label></div><div class="col-md-5">' +
    '<input class="form-control" type="text" name="Measure" size="30" placeholder="Measure..."> </div></div></div>');*/

 var structure = $('<div class="row"><div class="col-md-5">{{ sub_sub_form.as_p }}</div></div>')

 $('#part_order').append(structure);

})
