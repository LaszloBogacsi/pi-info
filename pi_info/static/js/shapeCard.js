$('.shape').shape();
$('.ui.checkbox').checkbox();
function flip(e, index, behaviour='flip over', arg2) {
    const shape = $(`.shape-${index}`).shape(behaviour, arg2);
    if (arg2) {
        shape.shape('flip over')
    }
    console.log("flippig" + index + behaviour)
}

function flipAndPrefillDetailsSide(e, index, schedule) {

    setTimeout(() => {
        const editSideElement = document.querySelector(`#schedule-edit-${index}`);
        const timeInputElement = editSideElement.querySelector('input[name=time]');
        timeInputElement.value = schedule.time;
        const scheduleIdInputElement = editSideElement.querySelector('input[name=schedule-id]');
        scheduleIdInputElement.value = schedule.schedule_id;

        $(`#schedule-edit-${index} .ui.checkbox:has(input[value=${schedule.status}])`).checkbox('check');
        const weekdays = $(`#schedule-edit-${index} .ui.checkbox:has(input[name=weekday])`);
        weekdays.each(function() {
           if (schedule.days.includes($(this).find('input').attr('value'))) {
                $(this).checkbox('check')
           }
        });
        console.log('hi')
    }, 500);
    flip(e, index);
}