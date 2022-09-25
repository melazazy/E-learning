document.addEventListener('DOMContentLoaded', () => {
    let num = document.getElementsByName("num");
    let cardvalue = document.getElementById("cardvalue");
    let check = document.getElementById("check");
    let btn = document.querySelector('.btn');
    let payaccount = document.querySelector('#paypalinput');

    document.querySelector('#paymenttype').addEventListener('change', function () {
        let v = document.querySelector('#visainput');
        let p = document.querySelector('#paypalinput');
        let vt = document.querySelector('.vtry');
        let pt = document.querySelector('.ptry');
        this.blur();
        if (this.value === 'visa') {
            p.setAttribute('disabled', 'true');
            p.innerHTML = '';
            pt.innerHTML = '';
            v.firstElementChild.focus();
            v.classList.remove('disabled_div');
            vt.innerHTML = 'try (4121 7565 3731 5570)';
        } else {
            v.classList.add('disabled_div');
            vt.innerHTML = '';
            vt.innerHTML = 'Try admin@example.com';
            p.removeAttribute('disabled');
            p.focus();
        }
    });
    for (let i = 0; i < num.length; i++) {
        num[i].onkeyup = function () {
            console.log((num[i].value).length);
            if (num[i].value !== '' & (num[i].value).length > 3) {
                num[i].blur();
                if (i === num.length - 1) {
                    let serial = "";
                    for (let i = 0; i < num.length; i++) {
                        serial += num[i].value;
                    }
                    // if (serial === "4121756537315570") {
                    if (serial === "4121756537315570") {
                        check.innerHTML = `<i class="fa-solid fa-check text-success"></i>`;
                        cardvalue.value = serial;
                        btn.removeAttribute('disabled');
                    } else {
                        btn.setAttribute('disabled', 'true');
                        check.innerHTML = `<i class="fa-solid fa-circle-xmark text-danger">`;
                    }
                } else {
                    num[i + 1].focus();
                }
            }
        };
    }
    payaccount.addEventListener('keyup', () => {
        if (payaccount.value === "admin@example.com") {
            btn.removeAttribute('disabled');
        }
        else {
            btn.setAttribute('disabled', 'true');
        }
    });

});


