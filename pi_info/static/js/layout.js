const sidebar_elem = $('#sidebar');
const pusher = $('.pusher');
pusher.width(((pusher.width() - 150) / pusher.width()) * 100 + '%');

sidebar_elem.sidebar({
    context: $('.ui.bottom.attached.segment'),
    dimPage: false,
    closable: false
});
function toggle_sidebar() {
    if (sidebar_elem.sidebar('is visible')) {
        sidebar_elem.sidebar('hide');
        pusher.animate({width: '100%'}, 500)

    } else {
        sidebar_elem.sidebar('show');
        pusher.animate({width: ((pusher.width() - 150) / pusher.width()) * 100 + '%'}, 500)
    }
}