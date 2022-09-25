document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#course_id').addEventListener('change', function () {
        fetch('/addlecturejson', {
            method: 'POST',
            body: JSON.stringify({
                course_id: document.querySelector('#course_id').value,
            })
        })
            .then(response => response.json())
            .then(data => {
                let select = document.querySelector('#lecture_id');
                select.innerHTML = '';
                select.innerHTML = `<option value="" selected> Select Lecture</option>`;
                data.forEach((o, i) => {
                    let op = document.createElement('option');
                    op.value = `${o['lecture_id']}`;
                    // op.dataset.id = `${i}`;
                    op.setAttribute('data-lecture_id', `${i}`);
                    op.innerHTML = `${o['lecture_title']}`;
                    select.append(op);
                });
                select.addEventListener('change', function (sel) {
                    let lselect = document.querySelector('#lesson_id');
                    lselect.innerHTML = '';
                    lselect.innerHTML = `<option value="" selected> Select Lesson</option>`;
                    console.log("this.dataset.id");
                    let id = $(this).find('option:selected').data('lecture_id');
                    data[id]['lesson'].forEach((l) => {
                        let op = document.createElement('option');
                        op.value = l['id'];
                        op.innerHTML = `${l['lesson_title']}`;
                        lselect.append(op);
                    });
                });
            });
        event.preventDefault();
    });

});
