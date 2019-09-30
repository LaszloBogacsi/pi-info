$('.ui.checkbox').checkbox();

function submitNew() {
    const devices_to_group = $("#new-group").find(".ui.checkbox.add-to-group")
        .filter(function () {
            return $(this).checkbox('is checked')
        }).map(function () {
            return Number(this.id)
        }).get();

    var input = $("<input>")
        .attr("type", "hidden")
        .attr("name", "ids").val(devices_to_group);
    $('form').append(input).submit();
}

function deselectAll() {
    $("#new-group").find(".ui.checkbox.add-to-group")
        .filter(function () {
            return $(this).checkbox('is checked')
        }).map(function () {
            return $(this).checkbox('uncheck')
        });
}