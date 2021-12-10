var form = $('form'),
    search = $('#search');

form.submit(function(e) {
    e.preventDefault();

    search.addClass('searching').val('');

    setTimeout(function() {
        search.removeClass('searching');
    }, 3600);
});

/* what's with input padding? :/ */
if ($.browser.mozilla) {
    search.css('padding', '3px');
}