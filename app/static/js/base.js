$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) &&
                !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});

const refreshURL = new URL('/refresh', window.origin);

function refreshToken(){
    $.ajax({
        url: refreshURL,
        method: "GET"
    });
}

var refreshTimerID = setTimeout(refreshToken, refreshTime);