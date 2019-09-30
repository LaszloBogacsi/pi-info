$('.ui.checkbox').checkbox();

function submitNew() {
    const parentElement = $("#new-group");
    const group_name = parentElement.find("input[name=group-name]").val();
    const delay_in_ms = Number(parentElement.find("input[name=delay-in-ms]").val());
    const devices_to_group = parentElement.find(".ui.checkbox.add-to-group")
        .filter(function () {
            return $(this).checkbox('is checked')
        }).map(function () {
            return Number(this.id)
        });

    const groupDataToSubmit = {
        group_name: group_name,
        delay_in_ms: delay_in_ms,
        device_ids: devices_to_group
    };
    const url = BASE_URL + "/lights/groups/save-new";

    submit(groupDataToSubmit, url);
}

function submit(data, url) {
    const requestInit = {
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify(data),
        redirect: 'follow',
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    };
    fetch(url, requestInit)
        .catch(error => {
            console.log(error);
        })
}

function deselectAll() {
    const parentElement = $("#new-group");
    parentElement.find(".ui.checkbox.add-to-group")
        .filter(function () {
            return $(this).checkbox('is checked')
        }).map(function () {
            return $(this).checkbox('uncheck')
        });
}