import { getFetch, loading } from "./utils.js";

const mainpage = document.querySelector("div.mainpage");
const desk_sidebar = document.querySelector("#desktop-sidebar");
const cover = document.querySelector("div.cover");
const dSch01 = document.querySelector("span#desktop-school01");
const dSch02 = document.querySelector("span#desktop-school02");
const dDor01 = document.querySelector("span#desktop-dormitory01");
const dDor02 = document.querySelector("span#desktop-dormitory02");
const dDor03 = document.querySelector("span#desktop-dormitory03");
let target = undefined;
let recent_script = undefined;
let version = {
    dSch01: 0,
    dSch02: 0,
    dDor01: 0,
    dDor02: 0,
    dDor03: 0,
}
let isOpened = true;

const removeScript = () => {
    if(recent_script != undefined){
        document.body.removeChild(recent_script);
    }
}

const fetchPage = async (e, file) => {
    loading(true);

    target = e.target;
    target.classList = "dreamBold blue";
    target.style = "text-decoration: underline";
    await getFetch({}, `http://127.0.0.1:6167/CSIAOnline/html(linux%20main%20page)/${file}.html`)
    .then(async res => await res.text())
    .then(html => {
        removeScript();

        let script = document.createElement("script");
        script.src = `./javascript/${file}.js?ver=${version["dDor01"]}`;
        script.type = "module";

        version[file] += 1;

        mainpage.innerHTML = html;
        document.body.appendChild(script);
    });

    loading(false);
}

document.getElementById("desktop-list").addEventListener('click', (e) => {
    if(isOpened){
        desk_sidebar.style.left = `${-desk_sidebar.clientWidth}px`;
        cover.style.gridTemplateColumns = '0 1fr';
    } else {
        cover.style.gridTemplateColumns = 'auto 1fr';
        desk_sidebar.style.left = `0px`;
    }
    isOpened = !isOpened;
});

dSch01.addEventListener("click", (e) => {
    fetchPage(e, "dSch01");
})

dSch02.addEventListener("click", (e) => {
    fetchPage(e, "dSch02");
})

dDor01.addEventListener("click", (e) => {
    fetchPage(e, "dDor01");
})

document.querySelector("div.rightHeaderSecond").addEventListener("click", async (e) => {
    loading(true);

    removeScript();

    if(target != undefined){
        target.classList = "";
        target.style = "text-decoration: none"
    }
    mainpage.innerHTML = '<img src="./image/배경화면.png" style="width: 100%;">';

    loading(false);
})