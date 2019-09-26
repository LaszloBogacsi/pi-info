$('.shape').shape();
$('.ui.checkbox').checkbox();

function flip(e, type, index, behaviour = 'flip over', arg2) {
    const shape = $(`.shape-${type}-${index}`).shape(behaviour, arg2);
    if (arg2) {
        shape.shape('flip over')
    }
    console.log("flippig" + index + behaviour)
}

function flipAndReset(e, type, index, behaviour = 'flip over', arg2) {
    resetSide(e, type, index);
    flip(e, type, index, behaviour, arg2);
}

function resetSide(e, type, index) {
    const DEFAULT_TIME = "18:00:00";

    setTime(document.querySelector(`#schedule-edit-${type}-${index}`), DEFAULT_TIME);

    $(`#schedule-edit-${type}-${index} .ui.checkbox:has(input[name=state])`).each(function() {
       $(this).checkbox('uncheck')
    });

    $(`#schedule-edit-${type}-${index} .ui.checkbox:has(input[name=weekday])`).each(function () {
        $(this).checkbox('uncheck')
    });
}

function flipAndPrefillDetailsSide(e, type, index, schedule) {
    // timeout to allow animation to finish
    setTimeout(() => {
        const editSideElement = document.querySelector(`#schedule-edit-${type}-${index}`);

        setTime(editSideElement, schedule.time);

        const scheduleIdInputElement = editSideElement.querySelector('input[name=schedule-id]');
        scheduleIdInputElement.value = schedule.schedule_id;

        $(`#schedule-edit-${type}-${index} .ui.checkbox:has(input[value=${schedule.status}])`).checkbox('check');
        const weekdays = $(`#schedule-edit-${type}-${index} .ui.checkbox:has(input[name=weekday])`);
        weekdays.each(function () {
            if (schedule.days.includes($(this).find('input').attr('value'))) {
                $(this).checkbox('check')
            }
        });
        console.log('hi')
    }, 500);
    flipAndReset(e, index);
}

function setTime(containingElement, value) {
    const timeInputElement = containingElement.querySelector('input[name=time]');
    timeInputElement.value = value;
}