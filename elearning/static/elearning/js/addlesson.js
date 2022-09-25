document.addEventListener('DOMContentLoaded', () => {
    let ltable = document.querySelector('#table-responsive');
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
                    // op.value = i + 1;
                    op.value = o['lecture_id'];
                    op.innerHTML = `${o['lecture_title']}`;
                    select.append(op);
                });
                select.addEventListener('change', function () {
                    ltable.innerHTML = `<table class="table">
                    <thead><tr><th scope="row">Lessons in Lecture</th></tr></thead>
                    <tbody id="table_tr"></tbody></table>`;
                    let row = document.createElement('tr');
                    let ttr = document.querySelector('#table_tr');
                    row.innerHTML = `<th>${data[(this.value) - 1]['lecture_title']} </th>`;
                    let lessons = document.createElement('td');
                    data[(this.value) - 1]['lesson'].forEach(a => {
                        let p = document.createElement('p');
                        p.innerHTML = `${a['lesson_title']}`;
                        lessons.append(p);
                    });
                    row.append(lessons);
                    ttr.append(row);
                });



            });
        event.preventDefault();
    });

});
