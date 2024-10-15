/**
 * Functions
 */

function closeForm() {
    if (typeof cusPopupFormElement !== 'undefined') {
        cusPopupFormElement.style.display = 'none';
    }
    if (typeof transPopupFormElement !== 'undefined') {
        transPopupFormElement.style.display = 'none';
    }
}

/**
 * Event Listeners
 */

window.onclick = function(e) {
    if (typeof cusPopupFormElement !== 'undefined' && e.target === cusPopupFormElement ) {
        cusPopupFormElement.style.display = 'none';
    } else if (typeof transPopupFormElement !== 'undefined' && e.target === transPopupFormElement ) {
        transPopupFormElement.style.display = 'none';
    }
}