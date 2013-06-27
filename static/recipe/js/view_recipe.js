$(function(){

    $('#star').raty({
        number: 5,
        score: function() {
            return $(this).attr('data-score');
        },
        readOnly: function() {
            return $(this).attr('data-user-vote') !== 'false';
        },
        noRatedMsg: "Not rated yet!",
        click: function(score, evt) {
            $.ajax({
                type: 'GET',
                url: window.location.href + 'rate/' + score + '/',
                success: function(data, textStatus, jqXHR){
                    console.log("Rating successfully added.");
                },
                error: function(jqXHR, textStatus, errorThrown){
                    if (errorThrown === "FORBIDDEN"){
                        console.log("Already voted.");
                    }
                    else {
                        console.log(errorThrown);
                    }
                }
            });
        }
    });
});
