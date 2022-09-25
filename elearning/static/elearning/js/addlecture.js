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
                ltable.innerHTML = `<table class="table">
                <thead>
                    <tr>
                        <th scope="row">Lecture</th>
                        <th scope="row">Lessons in Lecture</th>
                    </tr>
                </thead>
                <tbody id="table_tr">
                </tbody>
            </table>`;
                data.forEach(e => {
                    let row = document.createElement('tr');
                    let ttr = document.querySelector('#table_tr');
                    row.innerHTML = `<th>${e['lecture_title']} </th>`;
                    let lessons = document.createElement('td');
                    e['lesson'].forEach(a => {
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
