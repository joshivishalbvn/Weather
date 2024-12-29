function getCSRFToken() {
    var csrfToken = null;
    document.cookie.split(';').forEach(function(cookie) {
        if (cookie.trim().startsWith('csrftoken=')) {
            csrfToken = cookie.split('=')[1];
        }
    });
    return csrfToken;
}