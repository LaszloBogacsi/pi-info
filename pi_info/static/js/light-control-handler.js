function switchHandler(lightIds, currentStatus, index, delay, group_id) {
    const isGroup = !!group_id;
    const dataUrl = BASE_URL + "/lights/data" + (isGroup ? `?group_id=${group_id}` : `?light_id=${lightIds}`);

    loaderOn(index);
    fetch(dataUrl)
        .then(response => response.json())
        .then(data => {
            const status = isGroup ? data.group_status : data.single_device_status;
            const maybeParams = delay && group_id ? `&delay=${delay}&group_id=${group_id}` : '';
            const queryParams = `?light_ids=${lightIds}&status=${status}${maybeParams}`;
            const url = BASE_URL + "/lights/light-control";
            fetch(url + queryParams)
                .then(response => response.json())
                .catch(error => {
                    console.log(error);
                    loaderOff(index)
                })
                .then(data => {
                    handleResponse(data, index);
                    setTimeout(loaderOff, 500, index)

                });
        }).catch(error => {
        console.log(error);
        loaderOff(index)
    })


}

function handleResponse(res, index) {
    const status = JSON.parse(res[0]).status;
    console.log(res);
    const lightStatusElement = document.querySelector(`#light-status-${index}`);
    if (status === "ON") {
        lightStatusElement.classList.add("yellow")
    } else {
        lightStatusElement.classList.remove("yellow")
    }
}

function loaderOn(index) {
    const dimmerElement = document.querySelector(`#dimmer-${index}`);
    dimmerElement.classList.add("active");
}

function loaderOff(index) {
    const dimmerElement = document.querySelector(`#dimmer-${index}`);
    dimmerElement.classList.remove("active");
}