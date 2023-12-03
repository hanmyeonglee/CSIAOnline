/**
 * 인코딩된 문자열을 binary 타입으로 바꾸어서 전달하는 함수
 * @param {Array} u8Array 
 * @returns 인코딩된 문자열을 binary로 바꿔서 전달함
 */
export const uint8ArrayToBinary = (u8Array) => {
    let binaryString = '';
    for (let i = 0; i < u8Array.length; i++) {
        binaryString += String.fromCharCode(u8Array[i]);
    }
    return binaryString;
}

/**
 * 서버에서 public key를 받아오는 함수
 * @async
 * @returns 서버에서 public key를 받아와서 반환함
 */
export const fetchPublicKeyFromServer = async () => {
    let key = await fetch("http://127.0.0.1/CSIAOnline/AfterSchool/key/pubkey.pem")
    .then(async response => {
        return await response.text();
    });

    return key;
}

/**
 * 보내준 plain text를 pubkey를 통해 RSA 암호화해주는 함수
 * @param {String} pubkey -> 서버에서 받아온 public key를 넣으세요.
 * @param {String} plain  -> 보내려는 plain text(json 또는 그냥 text 등)을 넣으세요.
 * @returns 암호화 결과를 base64로 인코딩해서 전달함
 */
export const RSAEncryption = (pubkey, plain) => {
    let publicKey = forge.pki.publicKeyFromPem(pubkey);
        
    let secretMessage = uint8ArrayToBinary(new TextEncoder("utf-8").encode(plain));
    let encrypted = publicKey.encrypt(secretMessage, "RSA-OAEP", {
        md: forge.md.sha256.create(),
        mgf1: forge.mgf1.create()
    });

    let base64 = forge.util.encode64(encrypted);

    /* return forge.util.encode64(
        forge.pki.publicKeyFromPem(pubkey).encrypt(
            uint8ArrayToBinary(new TextEncoder("utf-8").encode(plain)),
            "RSA-OAEP",
            {
                md: forge.md.sha256.create(),
                mgf1: forge.mgf1.create()
            }
        )
    ); */

    return base64;
}