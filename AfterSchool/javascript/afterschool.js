import { postFetch, getFetch } from "./utils";

const base_link = location.href;

/**
 * user의 week schedule information에 대해 불러오는 함수
 * @param {String} session -> 서버에서 받은 session string을 사용한다.
 */
const fetchUserInformation = async (session) => {
    let result = await getFetch({
        "session": session
    }, base_link + "afterschool/getUserInformation")
    .then(async res => await res.json());
    
    return result;
}