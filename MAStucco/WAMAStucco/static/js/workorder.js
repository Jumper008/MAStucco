/**
 * Created by User on 01/03/2017.
 */

$("#cashed").click(function() {
   $('#').css("display", "none");
   $('#cashed_jobs').css("display", "block");
});

$("#taken").click(function() {
   $('#uncashed_jobs').css("display", "block");
   $('#cashed_jobs').css("display", "none");
});