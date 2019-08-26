$('.shape').shape();

function flip(e, index) {
    // console.log(e);
    // e.preventDefault();
    $(`.shape-${index}`).shape('flip over');
    console.log("flippig" + index)
}