light_state = {};

function switchHandler(lightId, currentStatus, index) {
    if (!light_state.hasOwnProperty(lightId)) {
        light_state[lightId] = {lightId, currentStatus, index};
    }
    const queryParams =  `?light_id=${lightId}&status=${light_state[lightId].currentStatus}`;
    const url = BASE_URL + "/lights/light-control";
    loaderOn(index);
    fetch(url + queryParams)
        .then(response => response.json())
        .catch(error => {
            console.log(error);
            loaderOff(index)
        })
        .then(data => {
            handleResponse(data, index);
            setTimeout(loaderOff, 1000, index)

        });
}

function handleResponse(res, index) {
    console.log(res);
    ({lightId, status} = {lightId: res.device_id, ...res});
    light_state[lightId] = {lightId, currentStatus: status, index};
    const lightStatusElement = document.querySelector(`#light-status-${index}`);
    console.log(lightStatusElement);
    if (res.status === "ON") {
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