$('.ui.checkbox').checkbox();
$(".ui.checkbox.add-to-group").checkbox('attach events', '.deselect.button', 'uncheck');

function submitNew() {
    const devices_to_group = $("#new-group").find(".ui.checkbox.add-to-group")
        .filter(function () {
            return $(this).checkbox('is checked')
        }).map(function () {
            return Number(this.id)
        }).get();

    const input = $("<input>")
        .attr("type", "hidden")
        .attr("name", "ids").val(devices_to_group);
    $('form').append(input).submit();
}

function submitEdit() {
    const devices_to_group = $("#edit-group").find(".ui.checkbox.add-to-group")
        .filter(function () {
            return $(this).checkbox('is checked')
        }).map(function () {
            return Number(this.id)
        }).get();

    const input = $("<input>")
        .attr("type", "hidden")
        .attr("name", "ids").val(devices_to_group);
    $('form').append(input).submit();
}

function preselectSome(ids) {
    $("#edit-group").find(".ui.checkbox.add-to-group")
        .filter(function () {
            return ids.includes(this.id)
        }).map(function () {
            return $(this).checkbox('check')
        });
}