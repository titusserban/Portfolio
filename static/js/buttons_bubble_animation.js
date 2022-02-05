const buttonSave = document.querySelector(".button-save");
const buttonCancel = document.querySelector(".button-cancel");


if (typeof(buttonSave) != 'undefined' && buttonSave != null) {
    buttonSave.addEventListener('click', function(e) {
            let x = e.clientX - e.target.offsetLeft;
            let y = e.clientY - e.target.offsetTop;

            let ripples = document.createElement('span');
            ripples.style.left = '0em';
            ripples.style.top =  '0em';
            this.appendChild(ripples);
            setTimeout(() => {
            ripples.remove()
        }, 1000);
    })
}


if (typeof(buttonCancel) != 'undefined' && buttonCancel != null) {
    buttonCancel.addEventListener('click', function(e) {
            let x = e.clientX - e.target.offsetLeft;
            let y = e.clientY - e.target.offsetTop;

            let ripples = document.createElement('span');
            ripples.style.left = '0em';
            ripples.style.top =  '0em';
            this.appendChild(ripples);
            setTimeout(() => {
            ripples.remove()
        }, 1000)
    });
}
