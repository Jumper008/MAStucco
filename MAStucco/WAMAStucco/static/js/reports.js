/**
 * Created by User on 01/03/2017.
 */

$("#chashedJ").click(function() {
   $('#uncashed_jobs').css("display", "none");
   $('#cashed_jobs').css("display", "block");
});

$("#unchashedJ").click(function() {
   $('#uncashed_jobs').css("display", "block");
   $('#cashed_jobs').css("display", "none");
});