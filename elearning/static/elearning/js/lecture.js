document.addEventListener('DOMContentLoaded', () => {
    let anslist = ['A'];
    // let studentlist = ["B", "c"];
    let studentlist = ["B"];
    // catch the ctrf from cookie
    function getCookie (cname) {
        let name = cname + "=";
        let ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return;
    }
    function loaddis (cid, lid) {
        fetch(`/discuss`, {
            method: 'POST',
            body: JSON.stringify({
                course_id: cid,
                lecture_id: lid,
            })
        })
            .then(response => response.json())
            .then(text => {
                console.log("discuss Text");
                console.log(text);
                // return text;
                // document.querySelector('#player').src = text['url'];
                // document.querySelector('#video').textContent = text['q2'];
                // document.querySelector('#content').innerHTML = `${text['q1']} ${text['q3']}`;
            });
    }
    function loaddiscuss (discuss, c_id, l_id) {
        console.log("discuss: ");
        console.log(discuss);
        console.log(c_id);
        console.log(l_id);
        let d = document.createElement('div');
        let form = document.createElement('form');
        let text = document.createElement('textarea');
        let inputElem = document.createElement('input');
        inputElem.type = 'hidden';
        inputElem.name = 'csrfmiddlewaretoken';
        inputElem.value = getCookie('csrftoken');
        form.append(inputElem);
        text.name = 'comment';
        form.append(text);
        form.method = 'POST';
        form.id = 'discuss';
        form.action = `/addcomment/${c_id}/${l_id}`;
        d.classList.add('questions');

        // for (let i = 0; i < discuss.length; i++) {
        for (let i = discuss.length - 1; i >= 0; i--) {
            console.log(discuss[i]['user_id'][0]);
            let question = document.createElement('div');
            question.innerHTML = `<img src="${discuss[i]['user_id'][0]['image']}" width="40px" alt="Student image"> <h3>${discuss[i]['user_id'][0]['username']}</h3>
            <p>${discuss[i]['comment']}</p><small>${discuss[i]['create']}</small>`;
            d.append(question);
        }
        // d.append(form)
        let button = document.createElement('button');
        button.setAttribute('type', 'submit');
        button.id = "check";
        button.classList.add('btn', 'btn-primary');
        button.innerHTML = "Add Comment";
        form.append(button);
        d.append(form);
        return d;

    }
    function loadquestions (x, y, z) {
        let questions = document.createElement('div');
        let form = document.createElement('form');
        let inputElem = document.createElement('input');
        inputElem.type = 'hidden';
        inputElem.name = 'csrfmiddlewaretoken';
        inputElem.value = getCookie('csrftoken');
        form.append(inputElem);
        form.method = 'POST';
        form.id = 'answers';
        form.action = '';
        questions.classList.add('questions');
        for (let i = 0; i < x.length; i++) {
            let question = document.createElement('div');
            question.innerHTML = `<h3>${x[i]['question']}</h3>`;
            for (let j = 0; j < 4; j++) {
                let options = document.createElement('div');
                let opnum = `option${j + 1}`;
                options.classList.add("form-check", "form-check-inline");
                options.innerHTML = `<input class="form-check-input" type="radio" name="option${i}"
                id="Radio${i}${j + 1}" value="${x[i][opnum]}">
            <label class="form-check-label" for="Radio${i}${j + 1}">${x[i][opnum]}</label>`;
                question.append(options);
            }
            anslist[i] = `${x[i]['answer']}`;
            form.append(question);
        }
        let button = document.createElement('button');
        button.setAttribute('type', 'submit');
        button.id = "check";
        button.value = x[0]['lesson_id'] > 0 ? 'Lesson' + x[0]['lesson_id'] : 'Lecture' + x[0]['lecture_id'];
        button.classList.add('btn', 'btn-primary');
        button.innerHTML = "Submit Answers";
        form.append(button);
        questions.append(form);
        return questions;
    }
    function iframe (id, src, width, height, frameborder, allow, fullscreen, allowfullscreen) {
        let iframe = document.createElement('iframe');
        iframe.id = id;
        iframe.src = src;
        iframe.setAttribute('width', width);
        iframe.setAttribute('height', height);
        iframe.setAttribute('frameborder', frameborder);
        iframe.setAttribute('allow', allow);
        iframe.setAttribute('fullscreen', fullscreen);
        iframe.setAttribute('allowfullscreen', allowfullscreen);

        return iframe;

    }
    function loadlesson (x, y, z) {
        fetch(`/loadlesson`, {
            method: 'POST',
            body: JSON.stringify({
                course_id: x,
                lecture_id: y,
                lesson_id: z,
            })
        })
            .then(response => response.json())
            .then(data => {
                data.forEach(e => {
                    if (typeof e['asks'] !== "undefined" && e['asks'] != '') {
                        e['asks'] = e['asks'].filter((x) => {
                            return x['lesson_id'].length == 0;
                        });
                    }
                    let main = document.querySelector('#lecture-section');
                    main.style.visibility = 'visible';
                    let h = document.createElement('h2');
                    let title;
                    if (e['lesson_title']) {
                        title = e['lesson_title'];
                        if (typeof e['lessonstate'] == "undefined" || e['lessonstate'].length < 1) {
                            // main.style.visibility = 'hidden';
                            let lock = document.createElement('div');
                            h.innerHTML = title;
                            lock.innerHTML = `<div class="well locked" style="background-color:transparent;border:none;box-shadow:none">
                            <center><div class="lecture-contents-locked" style="color:#454545;font-size:22px;font-weight:normal;font-style:normal;font-stretch:normal;line-height:2.05;text-align:center"><div class="locked-icon">
                                        <div class="lecture-lock-seal" style="background-image:url('//assets.teachablecdn.com/icons/star-seal.svg');display:inline-block;height:74px;position:relative;width:74px" >
                                            <div class="lecture-lock-seal-lock-icon" style="height:25px;margin:32px 0 0 26px;position:absolute;transform:rotate(0.0001deg);width:25px">
                                            <div class="main"></div>
                                            </div></div></div>Lesson content locked<div class="already-enrolled">You have to finish Previous Lesson And Answer his Questions correctly.</div></div></center></div>`;
                            main.innerHTML = '';
                            main.append(h);
                            main.append(lock);
                        } else {
                            h.innerHTML = title;
                            main.innerHTML = '';
                            main.append(h);
                            if (e['video_url']) {
                                main.append(iframe('player', e['video_url'], 640, 564, 0, 'autoplay', 'true', 'true'));
                            }
                            if (e['slide_url']) {
                                let p = document.createElement('p');
                                p.innerHTML = 'Slide Section: ';
                                main.append(p);
                                main.append(iframe('slider', e['slide_url'], 960, 569, '', '', 'true'));
                            }
                            if (e['doc_url']) {
                                let p = document.createElement('p');
                                p.innerHTML = 'Doc Section: ';
                                main.append(p);
                                main.append(iframe('doc', e['doc_url'], '100%', 569));
                            }
                            if (typeof e['questions'] !== "undefined" && e['questions'] != '') {
                                main.append(loadquestions(e['questions'], y, z));
                            }
                        }

                    } else {
                        title = e['lecture_title'];
                        if (typeof e['lecturestate'] == "undefined" || e['lecturestate'].length < 1) {
                            // main.style.visibility = 'hidden';
                            let lock = document.createElement('div');
                            h.innerHTML = title;
                            lock.innerHTML = `<div class="well locked" style="background-color:transparent;border:none;box-shadow:none">
                            <center><div class="lecture-contents-locked" style="color:#454545;font-size:22px;font-weight:normal;font-style:normal;font-stretch:normal;line-height:2.05;text-align:center"><div class="locked-icon">
                                        <div class="lecture-lock-seal" style="background-image:url('//assets.teachablecdn.com/icons/star-seal.svg');display:inline-block;height:74px;position:relative;width:74px" >
                                            <div class="lecture-lock-seal-lock-icon" style="height:25px;margin:32px 0 0 26px;position:absolute;transform:rotate(0.0001deg);width:25px">
                                            <div class="main"></div>
                                            </div></div></div>Lecture content locked<div class="already-enrolled">You have to finish Previous Lesson And Answer his Questions correctly.</div></div></center></div>`;
                            main.innerHTML = '';
                            main.append(h);
                            main.append(lock);
                        } else {
                            console.log("e['lecturestate']");
                            console.log(e['lecturestate']);
                            console.log(e['lecturestate'].length);
                            h.innerHTML = title;
                            main.innerHTML = '';
                            main.append(h);
                            if (e['video_url']) {
                                main.append(iframe('player', e['video_url'], 640, 564, 0, 'autoplay', 'true', 'true'));
                            }
                            if (e['slide_url']) {
                                main.append(iframe('slider', e['slide_url'], 960, 569, '', '', 'true'));
                            }
                            if (e['doc_url']) {
                                let p = document.createElement('p');
                                p.innerHTML = 'Doc Section: ';
                                main.append(p);
                                main.append(iframe('doc', e['doc_url'], '100%', 569));
                            }
                            if (typeof e['asks'] !== "undefined" && e['asks'] != '') {
                                main.append(loadquestions(e['asks'], y, z));
                            }
                            if (e['discuss']) {
                                main.append(loaddiscuss(e['discuss'], x, y));
                            }
                        }
                    }
                });
                document.querySelector('#check').addEventListener('click', function () {
                    let inputs = $(document.querySelector('#answers')).serializeArray();
                    for (let i = 1; i < inputs.length; i++) {
                        studentlist[i - 1] = `${inputs[i].value}`;
                    }
                    if (anslist.length === studentlist.length && anslist.every((value, index) => value === studentlist[index])
                    ) {
                        console.log("Correct Answer");
                        fetch(`/completestatus`, {
                            method: 'POST',
                            body: JSON.stringify({
                                course_id: x,
                                lecture_id: y,
                                lesson_id: z,
                            })
                        });
                        window.location.reload();

                    } else {
                        console.log("Wronge Anser");
                    }
                    event.preventDefault();
                });

            });
    }
    function loadassign (c, l) {
        fetch(`/assigne`, {
            method: 'POST',
            body: JSON.stringify({
                course_id: c,
                lecture_id: l,
            })
        })
            .then(response => response.json())
            .then(data => {
                let main = document.querySelector('#lecture-section');
                main.style.visibility = 'visible';
                let h = document.createElement('h2');
                let title;
                console.log("Data: ");
                console.log(data[0]);
                if (typeof data[0]['assignment_status'] == "undefined" || data[0]['assignment_status'].length < 1) {
                    title = data[0]['title'];
                    // main.style.visibility = 'hidden';
                    let lock = document.createElement('div');
                    h.innerHTML = title;
                    lock.innerHTML = `<div class="well locked" style="background-color:transparent;border:none;box-shadow:none">
                    <center><div class="lecture-contents-locked" style="color:#454545;font-size:22px;font-weight:normal;font-style:normal;font-stretch:normal;line-height:2.05;text-align:center"><div class="locked-icon">
                                <div class="lecture-lock-seal" style="background-image:url('//assets.teachablecdn.com/icons/star-seal.svg');display:inline-block;height:74px;position:relative;width:74px" >
                                    <div class="lecture-lock-seal-lock-icon" style="height:25px;margin:32px 0 0 26px;position:absolute;transform:rotate(0.0001deg);width:25px">
                                    <div class="main"></div>
                                    </div></div></div>Assignment content locked<div class="already-enrolled">You have to finish The Last Lesson in This Lecture And Answer his Questions correctly.</div></div></center></div>`;
                    main.innerHTML = '';
                    main.append(h);
                    main.append(lock);
                }
                else {
                    let main = document.querySelector('#lecture-section');
                    main.style.visibility = 'visible';
                    main.innerHTML = `<div class="assignments">
                <h3>${data[0]['title']}</h3>
                <p >${data[0]['description']}</p>
                <p class="description"></p></div`;
                    // let p = document.createElement('p');
                    let p = document.querySelector('.description');
                    let pform = document.createElement('p');
                    if (data[0]['image']) {
                        p.innerHTML = `<h4>Attachment Example </h4><img src="${data[0]['image']}" alt="attachment image" width="50%">`;
                    }
                    if (data[0]['answers'].length == 0) {
                        pform.innerHTML = `<form id="assform" action="/submitassigne" method="post">
                    <input type="hidden" name="${getCookie('csrftoken')}" value="">
                    <input type="hidden" name="id"  value="${data[0]['id']}">
                    <input type="text" name="answer" placeholder="Enter URL Here">
                    <button class="btn-primary" type="submit"> assign URL</button>
                </form>`;
                    }
                    else {
                        pform.innerHTML = 'You Already Submit Your Assignment';
                    }
                    p.append(pform);
                    // main.append(p);
                }
            });
    }

    document.querySelectorAll('.lecture').forEach(lec => lec.addEventListener('click', function () {
        let a = this.value;
        let navs = document.querySelectorAll(`.lesson${a}`);
        let ass = document.querySelectorAll(`.assign${a}`);
        navs.forEach(function (nav) {
            nav.classList.toggle('hide');
            nav.onclick = function () {
                loadlesson(this.dataset.course_id, a, this.value);
            };
        });
        ass.forEach(function (a) {
            a.classList.toggle('hide');
            a.onclick = function () {
                loadassign(this.dataset.course_id, this.dataset.lecture_id);
            };
        });

    }));

    document.querySelectorAll('.rating__input').forEach(e => e.addEventListener('click', function () {
        let input = document.querySelector('#rate');
        input.value = this.value;

    }));


    document.querySelector('.final').addEventListener('click', function () {
        c_id = document.querySelector('#course_final_id').value;
        fetch(`/loadfinal`, {
            method: 'POST',
            body: JSON.stringify({
                course_id: c_id,
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log(data[0]);
                main = document.querySelector('#lecture-section');
                main.innerHTML = '';
                h = document.createElement('h2');
                p = document.createElement('p');
                h.innerHTML = data[0]['title'];
                p.innerHTML = data[0]['description'];
                main.append(h);
                main.append(p);
                main.append(document.createElement('hr'));
                if (data[0]['video1_url']) {
                    h = document.createElement('h3');
                    h.innerHTML = 'Video 1';
                    main.append(h);
                    main.append(iframe('player', data[0]['video1_url'], 640, 564, 0, 'autoplay', 'true', 'true'));
                }
                if (data[0]['image1_url']) {
                    h = document.createElement('h3');
                    h.innerHTML = 'Image 1';
                    main.append(h);
                    img = document.createElement('img');
                    img.src = data[0]['image1_url'];
                    main.append(img);
                }
                if (data[0]['video2_url']) {
                    h = document.createElement('h3');
                    h.innerHTML = 'Video 2';
                    main.append(h);
                    main.append(iframe('player', data[0]['video2_url'], 640, 564, 0, 'autoplay', 'true', 'true'));
                }
                if (data[0]['image2_url']) {
                    h = document.createElement('h3');
                    h.innerHTML = 'Image 2';
                    main.append(h);
                    img = document.createElement('img');
                    img.src = data[0]['image2_url'];
                    main.append(img);
                }
                if (data[0]['submission'].length < 1) {
                    h = document.createElement('h2');
                    p = document.createElement('p');
                    h.innerHTML = 'Submit Your Final Project URL Below: ';
                    p.innerHTML = `<form id="assform" action="/submitfinal" method="post">
                        <input type="hidden" name="${getCookie('csrftoken')}" value="">
                        <input type="hidden" name="id"  value="${data[0]['id']}">
                        <input type="text" name="answer" placeholder="Enter URL Here">
                        <button class="btn-primary" type="submit"> assign URL</button>
                    </form>`;
                    main.append(h);
                    main.append(p);
                }
                else {
                    h = document.createElement('h2');
                    p = document.createElement('p');
                    h.innerHTML = 'Your Final Project URL Is: ';
                    p.innerHTML = `${data[0]['submission'][0]['answer']}`;
                    main.append(h);
                    main.append(p);
                }
            });

    });
    // document.querySelector('#check').addEventListener('click', function () {
    //     console.log("clicked Out of json");
    //     let inputs = $(document.querySelector('#answers')).serializeArray();
    //     console.log("inputs");
    //     console.log(inputs);
    //     for (let i = 1; i < inputs.length; i++) {
    //         studentlist[i - 1] = `${inputs[i].value}`;
    //     }
    //     console.log("studentlist");
    //     console.log(studentlist);
    //     if (anslist.length === studentlist.length && anslist.every((value, index) => value === studentlist[index])
    //     ) {
    //         console.log("Correct Answer");
    //     } else {
    //         console.log("Wronge Anser");
    //     }
    //     event.preventDefault();
    // });
});

