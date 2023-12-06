//import { fetchPublicKeyFromServer, RSAEncryption } from './crypto.js';
import { loading, errorHandling, getCookie, setCookie, deleteCookie, postFetch } from './utils.js';

const sessionAge = 604800;
const loginBtn = document.getElementById("login");
//const pubkey = await fetchPublicKeyFromServer();
const base_link = location.href;

/**
 * 화면에 들어왔을 때 session이 있는지 체크하는 함수
 * @async
 * @returns session이 있으면 session을 서버에 보내 검증한 결과를 반환하며, True일 경우 새로운 session을 등록한다. 만약 서버 오류나 False일 경우 undefined를 반환한다.
 * 
 * @todo : session hijacking 방지법 적용하기 
 */
export const sessionConfirm = async () => {
    let session = getCookie("CSIAOnlineSession");
    if(!session){
        return False;
    } else {
        let result = await postFetch(session, base_link + "account/session", "text/plain").then(response => {
            return response.json();
        });

        let operation = result["operation"];
        let body = result["body"];

        if(operation == "sessionConfirm" && body["result"]){
            setCookie("CSIAOnlineSession", body["content"], {"max-age":sessionAge});
            return body;
        } else {
            return undefined;
        }
    }
}

/**
 * id와 password를 입력하면 사용자가 맞는지 확인하는 함수
 * @async
 * @param {String} id -> input으로 입력받은 아이디를 넣어주세요
 * @param {String} pw -> 마찬가지로 패스워드를 입력해주세요
 * @returns 서버에 id와 pw를 보낸 결과를 T/F로 반환하고 True일 경우 session을 설정합니다. 만약 서버 오류일 경우 undefined를 반환합니다.
 * 
 * @todo : session hijacking 방지법 적용하기
 */
export const loginConfirm = async (id, pw) => {
    let plain = JSON.stringify(
        {
            "id":id,
            "pw":pw
        }
    );

    //let encrypted_text = RSAEncryption(plain);

    let result = await postFetch(plain, base_link + "account/login", "application/json").then(async response => {
        return await response.json();
    });

    let operation = result["operation"];
    let body = result["body"];

    if(operation == "loginConfirm"){
        if(body["result"]){
            setCookie('CSIAOnlineSession', result["content"], {"max-age":sessionAge});
        }
        return body["result"];
    } else {
        return undefined;
    }
}

//loginBtn.addEventListener("click", loginButtonEventFunction);