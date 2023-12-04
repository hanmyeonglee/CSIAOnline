/**
 * 로딩 화면을 보여주는 함수
 */
export const loading = () => {

}

/**
 * 화면에 띄워야 하는 오류가 있을 때 message를 주면 띄워주는 함수
 */
export const errorHandling = () => {
    
}

/**
 * 주어진 이름의 쿠키의 값을 반환하는 함수
 * @param {String} name -> 찾고자 하는 쿠키 이름을 적어주세요.
 * @returns 쿠키의 value가 반환됩니다. 쿠키가 없다면 undefined가 반환됩니다.
 */
export const getCookie = (name) => {
    let matches = document.cookie.match(
        new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

/**
 * cookie를 만들어주는 함수
 * @param {String} name -> 설정할 쿠키의 이름을 입력하세요.
 * @param {String} value -> 설정할 쿠키의 value를 입력하세요.
 * @param {Object} options -> 설정할 쿠키의 option(max-age, expires 등)을 object 형식으로 입력해주세요.
 */
export const setCookie = (name, value, options = {}) => {

    options = {
        path: '/', // 경로 지정
        ...options // 아규먼트로 옵션을 넘겨줬을경우 전개연산자로 추가 갱신
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString(); // 생 Date 객체라면 형식에 맞게 인코딩
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) { // 밸류가 없다면
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie; // 새로 갱신

}

/**
 * 특정한 Name의 쿠키를 삭제하는 함수
 * @param {String} name -> cookie 명을 입력해주세요.
 */
export const deleteCookie = (name) => { // 해당 쿠키 요소만 삭제
    setCookie(name, "", {
        'max-age': -1
    });
}

/**
 * 보내준 text를 서버에 전송하여 결과를 반환하는 함수
 * @async
 * @param {String} content -> Json 형식의 데이터를 입력해주세요.
 * @param {String} link -> POST를 보내려는 주소를 넣으세요.
 * @param {String} type -> 보내려는 데이터의 타입을 입력하세요.(textlain , application/json 등)
 * @returns content를 전송한 결과 Promise를 반환합니다.
 */
export const postFetch = async (content, link, type) => {
    return await fetch(`http://127.0.0.1/${link}`, {
        method: "POST",
        headers: {
            'Content-type': `${type}, charset=UTF-8`
        },
        body: content
    });
}