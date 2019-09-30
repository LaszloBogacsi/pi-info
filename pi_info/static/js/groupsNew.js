$('.ui.checkbox').checkbox();

function submitNew() {
    const parentElement = $("#new-group");
    const group_name = parentElement.find("input[name=group-name]").val();

    const groupDataToSubmit = {
        group_name: group_name
    }

}