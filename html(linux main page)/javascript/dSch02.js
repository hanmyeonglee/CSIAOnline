import { postFetch, getFetch, getCookie, copy, loading, alarm } from "./utils.js";

let rooms = {
    room1_1: false,
    room1_2: false,
    room1_3: false,
    room2_1: false,
    room2_2: false,
    room2_3: false,
    room3_1: false,
    room3_2: false,
    room3_3: false,
    room4_1: false,
    room4_2: false,
    room4_3: false,
    room5_1: false,
    room5_2: false,
    room5_3: false,
    room6_1: false,
    room6_2: false,
    room6_3: false,
}
const base = "http://127.0.0.1:8000/"
const page = document.querySelector("div.mainpage");
const applyBtn = page.querySelector("img#applySeminar");
const realBtn = page.querySelector("div#realBtn");
const modal = page.querySelector("div.modal-content");
const list = modal.querySelector("div.studentList");
const addBtn = modal.querySelector("div.addStudent");
const applyServerBtn = modal.querySelector("img.applyServer");
const session = getCookie("CSIAOnlineSession");
let temp_book_list = [];
let applyStudentNumber = 1;

// 여기부터는 함수

const pageSetter = async () => {
    loading(true);

    await (async () => {
        let isBooked = await getFetch({}, base + "afterschool/get_simple_seminar")
        .then(async res => await res.json())
        .catch((e) => {
            alarm(false, "서버와의 연결이 원활치 않습니다. 나중에 다시 시도해주십시오.");
        });

        if(isBooked['result']){
            isBooked = isBooked['content'];
        } else {
            alarm(false, "정보를 불러오는 도중 예기치 못한 문제가 발생했습니다. 재접속 해주십시오.");
            return;
        }

        for(let room of Object.keys(rooms)){
            let roomBlock = page.querySelector(`div#${room}`);
            if(isBooked[room]){
                roomBlock.classList.add("booked");
            } else {
                roomBlock.addEventListener("click", (element) => {
                    let target = element.target;
                    let id = target.id;
                    if(rooms[id]){
                        target.classList.remove("seminarSelect");   
                        temp_book_list = temp_book_list.filter((e) => {if(e == id) return false; else return true;});
                        rooms[id] = false;
                    } else {
                        target.classList.add("seminarSelect");
                        temp_book_list.push(room);
                        rooms[id] = true;
                    }
                });
            }
        }
    })();

    loading(false);
}

const formMaker = (flag=true) => {
    let cover = document.createElement("div");
    cover.classList = "studentForm mediumFont dreamBold blue";
    cover.id = `student0${applyStudentNumber}`;

    let div = document.createElement("div");
    div.classList = "number";
    div.innerText = applyStudentNumber;

    let numberInput = document.createElement("input");
    numberInput.classList = "studentNumber input smallFont dream black";
    numberInput.placeholder = "학번(Ex. 10101)";

    let nameInput = document.createElement("input");
    nameInput.classList = "studentName input smallFont dream black";
    nameInput.placeholder = "이름(Ex. 홍길동)";

    let deleteImg = document.createElement("img");
    deleteImg.src = "./image/bin.png";
    deleteImg.classList = "studentDelete headerSmallImg";
    deleteImg.value = applyStudentNumber;
    deleteImg.addEventListener("click", (e) => {
        let target = e.target;
        let p = target.parentElement;
        let pp = p.parentElement;

        for(let i = 2 ; i <= applyStudentNumber ; i++){
            if(i <= target.value){
                continue;
            }

            let tmpForm = pp.querySelector(`div#student0${i}`);
            tmpForm.id = `student0${i-1}`;
            tmpForm.querySelector("div.number").innerText = i-1;
            tmpForm.querySelector("img.studentDelete").value = i-1;
        }

        pp.removeChild(p);
        applyStudentNumber -= 1;
        addBtn.style = "display: block;";
    });

    cover.appendChild(div);
    cover.appendChild(numberInput);
    cover.appendChild(nameInput);
    cover.appendChild(deleteImg);

    return cover;
}

const resetter = () => {
    for(let tbl of temp_book_list){
        let tmp = page.querySelector(`div#${tbl}`);
        tmp.classList.remove("seminarSelect");
        tmp.classList.add("booked");
    }
    temp_book_list = [];
}

applyBtn.addEventListener("click", (e) => {
    if(temp_book_list.length > 0){
        realBtn.click();
    }

    let tmp = list.querySelector("div#student01");
    tmp.querySelector("input.studentNumber").value = "";
    tmp.querySelector("input.studentName").value = "";

    for(let i = 2 ; i <= applyStudentNumber ; i++){
        list.removeChild(list.querySelector(`div#student0${i}`));
    }
    applyStudentNumber = 1;
});

addBtn.addEventListener("click", (e) => {
    let target = e.target;
    
    applyStudentNumber += 1;
    let form = formMaker();
    list.insertBefore(form, addBtn);
    target.scrollIntoView({ behavior: 'smooth', block: 'end' });
    if(applyStudentNumber == 6){
        target.style = "display: none;";
    } else {
        target.style = "pointer-events: none;";
        setTimeout(() => {
            target.style = "pointer-events: all;";
        }, 250);
    }
});

applyServerBtn.addEventListener("click", async (e) => {
    loading(true);

    let regex = /^[1-3]0[1-4][0-2][0-9]$/;
    let send = {
        session: session,
        schedule: [
            copy(temp_book_list),
        ]
    }

    for(let i = 1 ; i <= applyStudentNumber ; i++){
        let tmpForm = list.querySelector(`div#student0${i}`);

        let studentNumber = tmpForm.querySelector("input.studentNumber").value;
        let studentName = tmpForm.querySelector("input.studentName").value;

        if(!regex.test(studentNumber) && studentName){
            alarm(false, "학번 포맷이 잘못되었습니다. 10101의 형태로 적어주십시오.");
            loading(false);
            return;
        }

        let grade = studentNumber[0];
        let classroom = studentNumber[2];
        let number = Number(studentNumber.substr(3, 2));

        send['schedule'].push({
            grade: grade,
            classroom: classroom,
            number: number,
            name: studentName,
        });
    }

    let result = await postFetch(JSON.stringify(send), base + "afterschool/set_seminar", 'application/json')
    .then(async response => await response.json())
    .catch((e) => {
        alarm(false, "서버와의 연결이 원활치 않습니다. 나중에 다시 시도해주십시오.");
    });

    if(!result['result']){
        alarm(false, result['content']);
        loading(false);
        return;
    }

    loading(false);
    alarm(true, "등록되었습니다.");
    modal.parentElement.querySelector("img.btn-close").click();
    resetter();
});

pageSetter();