import { alarm, postFetch, setCookie, loading } from './utils.js';

const base = "http://127.0.0.1:8000/";
const main = document.querySelector("div.login");
const id = main.querySelector("input.id");
const pw = main.querySelector("input.pw");
const loginBtn = main.querySelector("div.loginBtn");

loginBtn.addEventListener("click", async (e) => {
    loading(true);

    e.target.style = "pointer-events: none;";

    let idv = id.value;
    let pwv = pw.value;

    if(!pwv || !idv){
        alarm(false, "비밀번호를 입력해주십시오.");
        e.target.style = "pointer-events: all;";
        loading(false);
        return;
    }

    let send = {
        id: idv,
        pw: pwv,
    }

    let result = await postFetch(JSON.stringify(send), base + "account/tlogin", 'application/json')
    .then(async res => await res.json());

    if(!result['result']){
        e.target.style = "pointer-events: all;";
        alarm(false, result['content']);
    }
    else{
        let session = result['content'];
        setCookie("CSIAOnlineSession", session, {"max-age": 604800});
        alarm(true, "로그인 되었습니다.");
    }

    e.target.style = "pointer-events: all;";

    document.querySelector("div.main").style = "filter: none; pointer-events: all; user-select: auto;";
    document.querySelector("div.lrModal").style = "display: none";

    loading(false);
    return;
});