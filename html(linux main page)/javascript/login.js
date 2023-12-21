import { alarm, postFetch, setCookie, loading } from './utils.js';

const base = "http://127.0.0.1:8000/";
const main = document.querySelector("div.login");
const id = main.querySelector("input.id");
const pw = main.querySelector("input.pw");
const loginBtn = main.querySelector("div.loginBtn");
const registerBtn = main.querySelector("div.registerBtn");

const register = document.querySelector("div.register");
const nbs = register.querySelector("input.id");
const pws = register.querySelector("input.pw");
const names = register.querySelector("input.name");
const registerServer = register.querySelector("div.registerServer");
const backBtn = register.querySelector("img.backImg");

loginBtn.addEventListener("click", async (e) => {
    loading(true);

    e.target.style = "pointer-events: none;";

    let regex = /^[1-3]0[1-4][0-2][0-9]/;
    let idv = id.value;
    let pwv = pw.value;

    if(!regex.test(idv)){
        alarm(false, "id를 다시 입력해주십시오.");
        e.target.style = "pointer-events: all;";
        loading(false);
        return;
    }
    else if(!pwv){
        alarm(false, "비밀번호를 입력해주십시오.");
        e.target.style = "pointer-events: all;";
        loading(false);
        return;
    }

    let send = {
        id: idv,
        pw: pwv,
    }

    let result = await postFetch(JSON.stringify(send), base + "account/login", 'application/json')
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

registerBtn.addEventListener("click", (e) => {
    main.style = "display: none";
    register.style = "display: block";
});

registerServer.addEventListener("click", async (e) => {
    loading(true);

    e.target.style = "pointer-events: none;";

    let regex = /^[1-3]0[1-4][0-2][0-9]/;
    let snumber = nbs.value;
    let ppw = pws.value;
    let name = names.value;

    let grade = undefined;
    let classroom = undefined;
    let number = undefined;

    if(!regex.test(snumber)){
        alarm(false, "id를 다시 입력해주십시오.");
        e.target.style = "pointer-events: all;";
        loading(false);
        return;
    }
    else if(!ppw){
        alarm(false, "비밀번호를 입력해주십시오.");
        e.target.style = "pointer-events: all;";
        loading(false);
        return;
    }
    else if(!name){
        alarm(false, "이름을 입력해주십시오.");
        e.target.style = "pointer-events: all;";
        loading(false);
        return;
    }
    else{
        grade = snumber[0];
        classroom = snumber[2];
        number = snumber.substr(3, 2);
    }

    let send = {
        name: name,
        grade: grade,
        classroom: classroom,
        number: number,
        id: snumber,
        pw: ppw,
    }

    let result = await postFetch(JSON.stringify(send), base + "account/signup", 'application/json')
    .then(async res => await res.json());

    if(!result['result']){
        alarm(false, result['content']);
        e.target.style = "pointer-events: all;";
        loading(false);
        return;
    }
    else{
        let session = result['content'];
        setCookie("CSIAOnlineSession", session, {"max-age": 604800});
        alarm(true, "회원가입 되었습니다.");
    }

    e.target.style = "pointer-events: all;";

    main.style = "display: block";
    register.style = "display: none";
    loading(false);

    return;
})

backBtn.addEventListener("click", () => {
    main.style = "display: block";
    register.style = "display: none";
});