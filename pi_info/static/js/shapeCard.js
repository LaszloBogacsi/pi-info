$('.shape').shape();
$('.ui.checkbox').checkbox();
function flip(e, index, behaviour='flip over', arg2) {
    // console.log(e);
    e.preventDefault();
    const shape = $(`.shape-${index}`).shape(behaviour, arg2);
    if (arg2) {
        shape.shape('flip over')
    }
    console.log("flippig" + index + behaviour)
}