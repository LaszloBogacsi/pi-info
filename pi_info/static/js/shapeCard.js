$('.shape').shape();
$('.ui.checkbox').checkbox();

function flip(e, type, index, behaviour = 'flip over', arg2) {
    const shape = $(`.shape-${type}-${index}`).shape(behaviour, arg2);
    if (arg2) {
        shape.shape('flip over')
    }
    console.log("flippig" + index + behaviour)
}

function flipAndResetSchedule(e, type, index, behaviour = 'flip over', arg2) {
    resetScheduleSide(e, type, index);
    flip(e, type, index, behaviour, arg2);
}

function flipAndResetDeviceEdit(e, type, index, behaviour = 'flip over', arg2) {
    resetDeviceEditSide(e, type, index);
    flip(e, type, index, behaviour, arg2);
}

function flipAndPrefillScheduleDetailsSide(e, type, index, schedule, behaviour, arg2) {
    // timeout to allow animation to finish
    setTimeout(() => {
        const parentElement = $(`#schedule-edit-${type}-${index}`);
        setInputElementValue(parentElement.get()[0], "time", schedule.time);
        setInputElementValue(parentElement.get()[0], "schedule-id", schedule.schedule_id);
        setOneCheckBox(parentElement, schedule.status, "check");
        const weekdays = $(`#schedule-edit-${type}-${index} .ui.checkbox:has(input[name=weekday])`);
        weekdays.each(function () {
            if (schedule.days.includes($(this).find('input').attr('value'))) {
                $(this).checkbox('check')
            }
        });
    }, 500);
    flipAndResetSchedule(e, type, index, behaviour, arg2);
}

function flipAndPrefillDeviceDetailsSide(e, type, index, {device_id, name, location, device_type, ...rest}, behaviour, arg2) {
    // timeout  to allow animation to finish
    setTimeout(() => {
        const parentElement = $(`#device-edit-${type}-${index}`);
        setInputElementValue(parentElement.get()[0], "device_id", device_id);
        setInputElementValue(parentElement.get()[0], "name", name);
        setOneCheckBox(parentElement, device_type, "check");
        setOneCheckBox(parentElement, location, "check");
    }, 500);
    resetDeviceEditSide(e, type, index);
    flip(e, type, index, behaviour, arg2);
}


function resetScheduleSide(e, type, index) {
    const DEFAULT_TIME = "18:00:00";
    const parentElement = $(`#schedule-edit-${type}-${index}`);

    setInputElementValue(parentElement.get()[0], "time", DEFAULT_TIME);
    setAllCheckBox(parentElement, "state", "uncheck");
    setAllCheckBox(parentElement, "weekday", "uncheck");
}
function resetDeviceEditSide(e, type, index) {
    const parentElement = $(`#schedule-edit-${type}-${index}`);

    setAllCheckBox(parentElement, "type", "uncheck");
    setAllCheckBox(parentElement, "location", "uncheck");
}

function setAllCheckBox(parentElement, inputName, value) {
    parentElement.find(`.ui.checkbox:has(input[name=${inputName}])`).each(function () {
        $(this).checkbox(value)
    });
}

function setOneCheckBox(parentElement, inputValue, value) {
    parentElement.find(`.ui.checkbox:has(input[value="${inputValue}"])`).checkbox(value);
}

function setInputElementValue(parentElement, inputName, value) {
    const inputElement = parentElement.querySelector(`input[name=${inputName}]`);
    inputElement.value = value;
}
