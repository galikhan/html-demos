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

        if(qs.lesson && qs.lang) {

            document.getElementById("lesson-lang").innerHTML = qs.lang;
            
            // let domain = "https://mauthor.astanakitap.kz/ebook/json/";
            let domain = "http://localhost/mauthor-book/json/";
            const url =  domain + qs.lesson + "-" + qs.lang + ".json"
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
        }

    }catch(err) {
        console.error(err)
    }
};
LoadData();

function prepareChapterLink(chapterCount, chapter) {
    topics = Array.from(chapter.topics);
    link = "<a onclick='onChapterClick(" +chapterCount +")' id= " + chapterCount + " class='chapter list-group-item list-group-item-action list-group-item-light p-3' href='#!'>";
    link = link + chapter.title;
    // link = link + "<span class='badge badge-primary badge-pill'>"+ topics.length +"</span>";
    link = link + '</a>';
    return link;
}

function onChapterClick(id) {
    chapterDiv = document.getElementById("chapter-" + id);
    console.log('chapterDiv', chapterDiv);
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

    function readTextFile(file, callback) {
        var rawFile = new XMLHttpRequest();
        rawFile.overrideMimeType("application/json");
        rawFile.open("GET", file, true);
        rawFile.onreadystatechange = function() {
            if (rawFile.readyState === 4 && rawFile.status == "200") {
                callback(rawFile.responseText);
            }
        }
        rawFile.send(null);
    }
    
    //usage:
    // readTextFile("/Users/Documents/workspace/test.json", function(text){
    //     var data = JSON.parse(text);
    //     console.log(data);
    // });

});
