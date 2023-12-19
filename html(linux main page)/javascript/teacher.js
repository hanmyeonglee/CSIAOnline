import { getFetch, postFetch, loading, getCookie, alarm } from "./utils.js";

const mainpage = document.querySelector("div.mainpage");
const desk_sidebar = document.querySelector("#desktop-sidebar");
const cover = document.querySelector("div.cover");
const dtSch01 = document.querySelector("span#desktop-tschool01");
const dtSch02 = document.querySelector("span#desktop-tschool02");
const dtDor01 = document.querySelector("span#desktop-tdormitory01");
const dtDor02 = document.querySelector("span#desktop-tdormitory02");
const dtDor03 = document.querySelector("span#desktop-tdormitory03");
let target = undefined;
let recent_script = undefined;
let version = {
    dtSch01: 0,
    dtSch02: 0,
    dtDor01: 0,
    dtDor02: 0,
    dtDor03: 0,
}
let isOpened = true;
let session = getCookie("CSIAOnlineSession");
let info = undefined;

if(session){
    let tmp = await postFetch(session, "http://127.0.0.1/account/user_inform", "text/plain")
    .then(async res => res.json())
    .catch(e => alarm(false, "서버와의 연결이 원활치 않습니다. 나중에 다시 시도해주십시오."));

    if(tmp['result']){
        info = tmp['content'];
    } else {
        alarm(false, tmp['content']);
    }
}

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

dtSch01.addEventListener("click", (e) => {
    if(info){
        if(info['auth'].substr(6, 2) != "00"){
            fetchPage(e, "dtSch01");
            return;
        }
    }

    alarm(false, "로그인이 필요합니다.");
})

dtSch02.addEventListener("click", (e) => {
    if(info){
        if(info['auth'][7] == "1"){
            fetchPage(e, "dtSch02");
            return;
        }
    }

    alarm(false, "로그인이 필요합니다.");
})

dtDor01.addEventListener("click", (e) => {
    if(info){
        if(info['auth'][6] != "1"){
            fetchPage(e, "dtDor01");
            return;
        }
    }

    alarm(false, "로그인이 필요합니다.");
})

document.querySelector("div.rightHeaderSecond").addEventListener("click", async (e) => {
    loading(true);

    removeScript();

    if(target != undefined){
        target.classList = "";
        target.style = "text-decoration: none"
    }
    mainpage.innerHTML = '<img src="./image/배경화면.png" style="width: 100%; position: relative; top: -15%;">';

    loading(false);
})