let status = document.getElementById("orderStatus")
let csrftoken = getCookie('csrftoken');

status.addEventListener("input", function() {
    let newStatus = status.textContent
    let data = { status: newStatus }

    fetch('update_status/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(data),
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success: ', data)
    })
    .catch((error) => {
        console.error('My Error: ', error)
    })
}, false);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}