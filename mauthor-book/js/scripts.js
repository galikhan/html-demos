/*!
* Start Bootstrap - Simple Sidebar v6.0.5 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 
//
/* <a class="list-group-item list-group-item-action list-group-item-light p-3" href="#!">Dashboard</a>
<a class="list-group-item list-group-item-action list-group-item-light p-3" href="#!">Shortcuts</a>
<a class="list-group-item list-group-item-action list-group-item-light p-3" href="#!">Overview</a>
<a class="list-group-item list-group-item-action list-group-item-light p-3" href="#!">Events</a>
<a class="list-group-item list-group-item-action list-group-item-light p-3" href="#!">Profile</a>
<a class="list-group-item list-group-item-action list-group-item-light p-3" href="#!">Status</a> */


const LoadData = async () => {
    try {

        const url = 'http://localhost/mauthor-book/json/algebra.json'
        const res = await fetch(url);
        const data = await res.json();
        console.log();

        html = ""

        chapterCount = 0;
        Array.from(data.chapters, chapter => {
            console.log('chapter', chapter);
            html = html + prepareChapterLink(chapterCount, chapter);
            html = html + "<div style='display: none' id='chapter-" + chapterCount + "' class='list-group'>";
            Array.from(chapter.topics, topic => {
                console.log('topic', topic);
                html = html + "<a class='topics list-group-item list-group-item-action list-group-item-light p-3' href='#!'>" + topic.title + "</a>";                
            });
            html = html + "</div>";
            chapterCount++;
        });
        document.getElementById("menu").innerHTML = html;

        // data.chapters.array.forEach(element => {
        //     console.log(element);
        // });
    
    }catch(err) {
        console.error(err)
    }
};
LoadData();

function prepareChapterLink(chapterCount, chapter) {
    topics = Array.from(chapter.topics);
    link = "<a onclick='onChapterClick(" +chapterCount +")' id= " + chapterCount + " class='chapter list-group-item list-group-item-action list-group-item-light p-3' href='#!'>";
    link = link + chapter.title;
    link = link + "<span class='badge badge-primary badge-pill'>"+ topics.length +"</span>";
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
