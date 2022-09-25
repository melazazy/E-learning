document.addEventListener('DOMContentLoaded', () => {
    console.log("From Index");
    document.querySelector('#fillterbtn').addEventListener('click', function () {
        filltercourses();
        event.preventDefault();
    });
    function filltercourses () {
        // fetch(`/filter`) 
        fetch('/filter', {
            method: 'POST',
            body: JSON.stringify({
                cat: document.querySelector('#cat').value,
                price: document.querySelector('#price').value,
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.length == 0) {
                    document.querySelector('.courses').innerHTML = `<p>No courses du Your Options</p><p>Try Another Fillter Options</p>`;
                }
                else {
                    document.querySelector('.courses').innerHTML = '';
                }
                data.forEach(function (c, i) {
                    let cdiv = document.createElement('div');
                    cdiv.classList.add('course_block');
                    // cdiv.innerHTML = "Testing";
                    let startp = '', b, p, rates = 0.0, raters = 0;
                    console.log("c['students'.length]");
                    console.log(c['students'].length);
                    // console.log(c['students'][0]['rate_scale']);
                    for (let i = 0; i < c['students'].length; i++) {
                        console.log(i + ')' + parseFloat(c['students'][i]['rate_scale']));
                        if (parseFloat(c['students'][i]['rate_scale']) >= 0) {
                            rates += parseFloat(c['students'][i]['rate_scale']);
                            raters++;
                        }
                        console.log(i + ')' + rates);
                    }
                    console.log("rates");
                    console.log(rates);
                    if (rates > 0) {
                        rates = `(${rates / raters} out of 5)`;
                    } else {
                        rates = "(Not Rating)";
                    }
                    if (parseInt(c['price']) > 0) {
                        p = `<span style="color: green;">${(c['price'])} $</span>`;
                    } else {
                        p = `<span style="color: green;"> Free </span>`;
                    }
                    if (parseInt(c['start_price']) > 0) {
                        startp = `<span style="color: red;"><s><span>E£${(c['start_price'])}</span></s></span>`;
                    }
                    if (c['best_seller']) {
                        b = `<p class="bSeller bSellerText">Best Seller</p>`;
                    } else {
                        b = `<p class="bSeller"></p>`;
                    }
                    cdiv.innerHTML = `
                        <a href="/course/${c['course_id']}" class="nav-link course_block-link">
                            <div class="img">
                                <img src="${c['image_url']}" alt="Course Image" width="240" height="135">
                            </div>
                            <h3>${c['course_title']}</h3>
                            <p>${c['teacher'][0]['username']}</p>
                            <p><span class="">Rating: ${rates} </span><span aria-label="" class="">${raters} <small>
                            Rating</small></span></p>
                            <p>${p} ${startp}</p>
                            ${b}
                        </a>`;
                    let course = document.querySelector('.courses').append(cdiv);
                });

            });
    }
});


/*
Card number:
4121 7565 3731 5570
PIN:
943
Name:
Murphy Rochia
Address:
3590 College way
Country:
USA
CVV:
939
Expiration date:
05/2022
*/