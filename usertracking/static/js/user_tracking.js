

$.ajaxSetup({beforeSend: function(xhr, settings){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
}});


/* hook to do client side verification if needed */
$(function(){
    // check if cookie verification is set
    // trigger a get to set csrf token

    if ($.cookie('user_tracking_verify') !== null){
        $.post('/user-tracking/verify');
    }
});



var user_tracking = (function(){

    var register_event = function(eventName, eventData){
        if ($.cookie('user_tracking_id') !== null){

            var event_data_json = JSON.stringify(eventData, null);

            $.post('/user-tracking/register-event', { event_name: eventName , event_data : event_data_json});
        }
    };


    // Return an object that exposes our public api function publicly
    return {
        register_event: register_event
    };

})();
