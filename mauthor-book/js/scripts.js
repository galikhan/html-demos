var qs = (function (a) {
    if (a == "") return {};
    var b = {};
    for (var i = 0; i < a.length; ++i) {
        var p = a[i].split('=', 2);
        if (p.length == 1)
            b[p[0]] = "";
        else
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return b;
})(window.location.search.substr(1).split('&'));


const LoadData = async () => {

    try {

        if (qs.lesson && qs.lang) {

            // document.getElementById("lesson-lang").innerHTML = qs.lang;
            let domain = "https://mauthor.astanakitap.kz/ebook/json/";
            // let domain = "http://localhost/mauthor-book/json/";
            const url = domain + qs.lesson + "-" + qs.lang + ".json"
            const res = await fetch(url);
            const data = await res.json();
            html = ""
            chapterCount = 0;
            Array.from(data.chapters, chapter => {
                html = html + prepareChapterLink(chapterCount, chapter);
                html = html + "<div style='display: none' id='chapter-" + chapterCount + "' class='list-group'>";
                Array.from(chapter.topics, topic => {
                    html = html + "<a class='topics list-group-item list-group-item-action list-group-item-light' href='" + topic.url + "' target='iframe_a'>" + topic.title + "</a>";
                });
                html = html + "</div>";
                chapterCount++;
            });
            document.getElementById("menu").innerHTML = html;

        } else {

            lesson = document.getElementById("lessonType");
            books = getBooksByLessonName(lesson.value);
            html = "";
            Array.from(books, book => {
                html = html + '<div class="card">';
                html = html + '<div class="card-body">';
                html = html + '<h5 class="card-title">' + book.title + '</h5>';
                html = html + '</div>';
                html = html + '<ul class="list-group list-group-flush">';
                html = html + '<li class="list-group-item">' + book.title + '</li>';
                html = html + '<li class="list-group-item">' + book.class + '</li>';
                html = html + '<li class="list-group-item">' + book.author + '</li>';
                html = html + '<li class="list-group-item">' + book.lang + '</li>';
                html = html + '</ul>';
                html = html + '<div class="card-body">';
                html = html + '<a href="index.html?lesson=' + book.lesson + '&lang=' + book.lg + '" class="btn btn-primary card-link">';
                html = html + 'кіру';
                html = html + '</a>';
                html = html + '</div>';
                html = html + '</div>';
            });

            document.getElementById("books").innerHTML = html
        }

    } catch (err) {
        console.error(err)
    }
};
LoadData();

function prepareChapterLink(chapterCount, chapter) {
    topics = Array.from(chapter.topics);
    link = "<a onclick='onChapterClick(" + chapterCount + ")' id= " + chapterCount + " class='chapter list-group-item list-group-item-action list-group-item-light p-3' href='#!'>";
    link = link + chapter.title;
    // link = link + "<span class='badge badge-primary badge-pill'>"+ topics.length +"</span>";
    link = link + '</a>';
    return link;
}

function onChapterClick(id) {
    chapterDiv = document.getElementById("chapter-" + id);
    if (chapterDiv.style.display === "none") {
        chapterDiv.style.display = "block";
    } else {
        chapterDiv.style.display = "none";
    }
}

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        if (localStorage.getItem('mauthor-sidebar-toggle') === 'true') {
            document.body.classList.toggle('sb-sidenav-toggled');
        }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('mauthor-sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
});


function getBooksByLessonName(lesson) {
    lessons = {
        "algebra": [
            {
                "title": "Algebra 8 textbook",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі:  english",
                "lg": "en",
                "lesson": "algebra"
            },
            {
                "title": "Алгебра 8 оқулығы",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі:  қазақша",
                "lg": "qq",
                "lesson": "algebra"
            }
        ],
        "geometry": [
            {
                "title": "Geometry 8 textbook",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі:  english",
                "lg": "en",
                "lesson": "geometry"

            },
            {
                "title": "Геометрия 8 оқулығы",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі:қазақша"
                , "lg": "qq",
                "lesson": "geometry"

            }
        ],
        "informatics": [
            {
                "title": "Informatics 8 textbook",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  english"
                , "lg": "en",
                "lesson": "informatics"
            }, {
                "title": "Информатика 8 оқулығы",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  қазақша"
                , "lg": "qq",
                "lesson": "informatics"

            }, {
                "title": "Информатика 8 учебник",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  на русском языке"
                , "lg": "ru",
                "lesson": "informatics"

            }, {
                "title": "Informatics 8 қостілді оқулық",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  қазақша-ағылшынша"
                , "lg": "en-qq",
                "lesson": "informatics"

            }, {
                "title": "Informatics  8 билингвальный учебник",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  русско-английский"
                , "lg": "en-ru",
                "lesson": "informatics"

            }],
        "biology":
            [
                {

                    "title": "Biology 8 textbook",
                    "class": "Сыныбы: 8",
                    "author": "Авторлары:  -",
                    "lang": "Оқыту тілі  english"
                    , "lg": "en",
                    "lesson": "biology"

                }, {

                    "title": "Биология 8 оқулығы",
                    "class": "Сыныбы: 8",
                    "author": "Авторлары:  -",
                    "lang": "Оқыту тілі  қазақша"
                    , "lg": "qq",
                    "lesson": "biology"

                }, {

                    "title": "Биология 8 учебник",
                    "class": "Сыныбы: 8",
                    "author": "Авторлары:  -",
                    "lang": "Оқыту тілі  на русском языке",
                    "lg": "ru",
                    "lesson": "biology"


                }, {

                    "title": "Biology 8 қостілді оқулық",
                    "class": "Сыныбы: 8",
                    "author": "Авторлары:  -",
                    "lang": "Оқыту тілі  қазақша-ағылшынша"
                    , "lg": "en-qq",
                    "lesson": "biology"

                }, {

                    "title": "Biology 8 билингвальный учебник",
                    "class": "Сыныбы: 8",
                    "author": "Авторлары:  -",
                    "lang": "Оқыту тілі  русско-английский"
                    , "lg": "en-ru",
                    "lesson": "biology"


                }
            ],
        "physics": [
            {

                "title": "Physics 8 textbook",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  english",
                "lg": "en",
                "lesson": "physics"

            }, {

                "title": "Физика 8 оқулығы",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  қазақша",
                "lg": "qq",
                "lesson": "physics"

            }, {

                "title": "Физика 8 учебник",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  на русском языке",
                "lg": "ru",
                "lesson": "physics"

            }, {

                "title": "Physics 8 қостілді оқулық",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  қазақша-ағылшынша",
                "lg": "en-qq",
                "lesson": "physics"
            }, {


                "title": "Physics 8 билингвальный учебник",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  русско-английский",
                "lg": "en-ru",
                "lesson": "physics"

            }],
        "chemistry": [
            {
                "title": "Chemistry 8 textbook",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  english",
                "lg": "en",
                "lesson": "chemistry"

            }, {

                "title": "Химия 8 оқулығы",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  қазақша",
                "lg": "qq",
                "lesson": "chemistry"

            }, {

                "title": "Химия 8 учебник",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  на русском языке",
                "lg": "ru",
                "lesson": "chemistry"
            }, {

                "title": "Chemistry 8 қостілді оқулық",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  қазақша-ағылшынша",
                "lg": "en-qq",
                "lesson": "chemistry"

            }, {

                "title": "Chemistry 8 билингвальный учебник",
                "class": "Сыныбы: 8",
                "author": "Авторлары:  -",
                "lang": "Оқыту тілі  русско-английский",
                "lg": "en-ru",
                "lesson": "chemistry"

            }
        ]
    }
    return lessons[lesson];
}