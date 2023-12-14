import { postFetch, getFetch, getCookie, getWeek, copy, diffDate, loading } from "./utils.js";

loading(true);

const base = "http://127.0.0.1:8000/";
const page = document.querySelector("div.dSch01Cover");
const uls = page.querySelectorAll("div.mainCover > div > ul.dropdown-menu");
const days = {
    mon: page.querySelector("div.mon"),
    tue: page.querySelector("div.tue"),
    wed: page.querySelector("div.wed"),
    thr: page.querySelector("div.thr"),
};
const days_list = ['mon', 'tue', 'wed', 'thr'];
const modal = page.querySelector("div.modal-content.auto");
const fixed_days = {
    mon_fixed: modal.querySelector("div.mon"),
    tue_fixed: modal.querySelector("div.tue"),
    wed_fixed: modal.querySelector("div.wed"),
    thr_fixed: modal.querySelector("div.thr"),
}
const fixed_days_list = ['mon_fixed', 'tue_fixed', 'wed_fixed', 'thr_fixed'];
const list = document.createElement("div");
const drarrow = page.querySelector("img#desktopRightArrow");
const dlarrow = page.querySelector("img#desktopLeftArrow");
const autowrite = page.querySelector("div.autoWrite");
let present = new Date();
let session = getCookie("CSIAOnlineSession");
list.classList = "classInfo dream smallFont";

let all_lesson_byid = {};
let all_lesson = {'mon':[[], [], []], 'tue': [[], [], []], 'wed': [[], [], []], 'thr': [[], [], []]};
let user_inform = await postFetch(JSON.stringify({
    session: session,
}), base + "afterschool/afterschool_user_inform", "application/json")
.then(async res => {
    let tmp = await res.json();
    return tmp['content'];
});

/**
 * date 주면 그 날짜가 포함된 주의 user의 nightschedule을 {'mon' : {schedule:~, id:~} ...}의 형태로 반환함
 * @param {Date} date : 오늘 날짜 하면 자동으로 월요일 날짜 계산해서 이번주 어쩌고 저쩌고 ㅋㅋ
 * @async
 */
const weekGetter = async (date) => {
    loading(true);

    let day = date.getDay();

    let temp_mon = new Date(date);
    temp_mon.setDate(date.getDate() - day + 1);

    let schedule_week = await postFetch(JSON.stringify({
        session: session,
        date: `${temp_mon.getFullYear()}-${temp_mon.getMonth() + 1}-${temp_mon.getDate()}`,
    }), base + "afterschool/schedule", 'application/json')
    .then(async res => {
        let tmp = await res.json();
        return tmp
    });
    
    console.log("-------")
    console.log(schedule_week);
    console.log("-------")

    if(schedule_week['result']){
        schedule_week['content']['crit'] = temp_mon;
        loading(false);
        
        return schedule_week['content'];
    } else {
        alert("페이지 로딩 중 예상치 못한 오류가 발생했습니다. 재접속해주세요.");
    }

}

/**
 * 세팅할 날짜를 보내면 받아서 그 주의 야자 4교시 일정을 세팅해줌.
 * @param {Date} date : present 변수를 보내는 것으로 대신함. 세팅할 날짜를 말함.
 */
const weekSetter = async (date) => {
    let week = await weekGetter(date);
    
    page.querySelector("div.week").innerText = `< ${week['crit'].getMonth() + 1}월 ${getWeek(new Date(week['crit']))}주 >`;
    for(let d of days_list){
        let day = days[d].querySelector("div.date");
        
        day.innerText = `${week['crit'].getMonth() + 1}.${week['crit'].getDate().toString().padStart(2, '0')}`;
        day.setAttribute("cls-ids", week[d]['schedule']);
        let schedules = week[d]['schedule'].split("/");
        for(let idx of [0, 1, 2]){
            let fixed_day_inp = days[d].querySelector(`div.innerText[value='${idx+1}']`);
            if(schedules[idx] == "0"){
                fixed_day_inp.innerText = "야자";
            } else if(schedules[idx] == "1"){
                fixed_day_inp.innerText = "조퇴";
            } else if(schedules[idx] == "-1"){
                fixed_day_inp.innerText = "외출";
            } else{
                fixed_day_inp.innerText = `${all_lesson_byid[schedules[idx]]['class_type']} (${all_lesson_byid[schedules[idx]]['class_location']})`;
            }
        }
        
        week['crit'].setDate(week['crit'].getDate() + 1);
    }
}

/**
 * 초기 페이지 세팅,
 * 모든 수업을 불러와서,
 * 첫째 id에 대한 class 정보로 정리하고
 * 둘째 date에 대한 class 정보로 정리하여 변수에 저장한다.
 */
await getFetch({}, base + "afterschool/all_class")
.then(async res => await res.json())
.then(classes => {
    classes = classes['content'];
    console.log(classes);
    all_lesson_byid = copy(classes);
    for(let [id, cls] of Object.entries(classes)){
        const regex1 = /^1[01]{3}$/;
        const regex2 = /^[01]1[01]{2}$/;
        const regex3 = /^[01]{2}1[01]$/;
        cls['id'] = id;
        let temp = cls['class_time'].split(";");

        for(let i = 0 ; i < temp.length ; i++){
            let time = temp[i].trim();
            if(time){
                let tmp = time.split(" ");
                if(regex1.test(tmp[1])){
                    all_lesson[tmp[0]][0].push(copy(cls));
                }
                
                if(regex2.test(tmp[1])){
                    all_lesson[tmp[0]][1].push(copy(cls));
                }

                if(regex3.test(tmp[1])){
                    all_lesson[tmp[0]][2].push(copy(cls));
                }
            }
        }

        // 최종적으로 all_lesson은 {'mon':[{classname:~, classlocation:~, classtime: ~, id:~, teacher: ~, classtype:~} ...] ...}의 형태를 띈다.
    }
    
    console.log("---all_lesson---")
    console.log(all_lesson);
    console.log("---user_inform---")
    console.log(user_inform);
});

/**
 * 초기 페이지 세팅
 * present 변수는 초기 시작점에서 오늘의 값을 가짐.
 */
await weekSetter(new Date(present));

console.log('start');

/**
 * 초기 페이지 세팅,
 * 네 개 칸에 있는 드롭다운에 대해 이벤트를 지정해줌
 * 첫 번째 칸은 클릭하면 조퇴로 신청 -> 칸의 글씨도 바뀜,
 * 두 번째 칸은 클릭하면 야자로 신청 -> 칸의 글씨도 바뀜,
 * 세 번째 칸은 클릭하면 모달 뜨면서 선택할 주문형/CSMP/방과후 선택함  -> 칸의 글씨도 바뀜
 */
for(let ul of uls){
    let day = ul.parentElement.querySelector("div.date");
    let temp_date = day.innerText.trim().split(".");
    let idx = ul.getAttribute("cls-time");
    for(let li of ul.querySelectorAll("li[value='1']")){
        li.addEventListener("click", async (e) => {
            loading(true);

            let target = e.target;
            console.log(day);
            let cls_ids = day.getAttribute("cls-ids").split("/");

            for(let i of [0, 1, 2]){
                cls_ids[i] = "1"
            }
            let req = cls_ids.join("/");

            let server_result = await postFetch(JSON.stringify({
                session: session,
                temp_schedule: req,
                date: `${present.getFullYear()}-${temp_date.join("-")}`,
            }), base + "afterschool/temp", "application/json")
            .then(async res => await res.json());

            console.log(server_result);
            
            if(server_result['result']){
                for(let i of [1, 2, 3]){
                    target.parentElement.parentElement.querySelector(`div.innerText[value='${i}']`).innerText = "조퇴";//target.innerText;
                }
                day.setAttribute("cls-ids", req);
            } else {
                alert("실패, 재시도 요망");
            }

            loading(false);
        });
    }

    for(let li of ul.querySelectorAll("li[value='2']")){
        li.addEventListener("click", async (e) => {
            loading(true);

            let target = e.target;
            let cls_ids = day.getAttribute("cls-ids").split("/");

            for(let i of [0, 1, 2]){
                cls_ids[i] = "-1"
            }
            let req = cls_ids.join("/");
            
            let server_result = await postFetch(JSON.stringify({
                session: session,
                temp_schedule: req,
                date: `${present.getFullYear()}-${temp_date.join("-")}`,
            }), base + "afterschool/temp", "application/json")
            .then(async res => await res.json());

            console.log(server_result);

            if(server_result['result']){
                for(let i of [1, 2, 3]){
                    target.parentElement.parentElement.querySelector(`div.innerText[value='${i}']`).innerText = "외출";//target.innerText;
                }
                day.setAttribute("cls-ids", req);
            } else {
                alert("실패, 재시도 요망");
            }

            loading(false);
        });
    }

    for(let li of ul.querySelectorAll("li[value='3']")){
        li.addEventListener("click", async (e) => {
            loading(true);

            let target = e.target;
            let cls_ids = day.getAttribute("cls-ids").split("/");

            let not_study_idx = [];
            for(let i of [0, 1, 2]){
                if(cls_ids[i] == "1" || cls_ids[i] == "-1" || i == idx){
                    cls_ids[i] = "0";
                    not_study_idx.push(i);
                }
            }
            let req = cls_ids.join("/");
            
            let server_result = await postFetch(JSON.stringify({
                session: session,
                temp_schedule: req,
                date: `${present.getFullYear()}-${temp_date.join("-")}`,
            }), base + "afterschool/temp", "application/json")
            .then(async res => await res.json());

            console.log(server_result);

            if(server_result['result']){
                for(let i of not_study_idx){
                    target.parentElement.parentElement.querySelector(`div.innerText[value='${i+1}']`).innerText = "야자";//target.innerText;
                }
                target.parentElement.parentElement.querySelector("div.innerText[value='3']").innerText = "야자";//target.innerText + `(5${grade}${classroom}호)`;
                day.setAttribute("cls-ids", req);
            } else {
                alert("실패, 재시도 요망");
            }

            loading(false);
        });
    }

    for(let li of ul.querySelectorAll("li[value='4']")){
        li.addEventListener("click", (e) => {
            page.querySelector("div.order.scheduleList.select").innerHTML = "";
            page.querySelector("div.afterschool.scheduleList.select").innerHTML = "";
            page.querySelector("h5.select.modal-title").innerText = ul.parentElement.querySelector("div.weekday").innerText + ' ' + ul.parentElement.querySelector("div.date").innerText;
            let day_cll = ul.parentElement.classList.toString();
            let classes = undefined;
            if(day_cll.includes('mon')){
                classes = all_lesson['mon'][idx];
            } else if(day_cll.includes('tue')){
                classes = all_lesson['tue'][idx];
            } else if(day_cll.includes('wed')){
                classes = all_lesson['wed'][idx];
            } else if(day_cll.includes('thr')){
                classes = all_lesson['thr'][idx];
            }
    
            for(let cls of classes){
                let cp = list.cloneNode();
                cp.id = cls['id'];
                cp.innerText = `${cls['class_location']} : ${cls['teacher']} ${cls['class_name']}`;
                if(cls['class_type'] == "주문형"){
                    page.querySelector("div.order.scheduleList.select").appendChild(cp);
                } else if(cls['class_type'] == "방과후"){
                    page.querySelector("div.afterschool.scheduleList.select").appendChild(cp);
                }

                cp.addEventListener("click", async () => {
                    loading(true);
                    console.log(day);

                    let cls_ids = day.getAttribute("cls-ids").split("/");
                    let not_study_idx = [];

                    for(let i of [0, 1, 2]){
                        if(cls_ids[i] == "1" || cls_ids[i] == "-1"){
                            cls_ids[i] = "0";
                            not_study_idx.push(i);
                        }
                    }
                    cls_ids[idx] = cp.id;

                    let req = cls_ids.join("/");

                    let server_result = await postFetch(JSON.stringify({
                        session: session,
                        temp_schedule: req,
                        date: `${present.getFullYear()}-${temp_date.join("-")}`,
                    }), base + "afterschool/temp", "application/json")
                    .then(async res => await res.json());

                    console.log(server_result);
        
                    if(server_result['result']){
                       // let index = Number(li.parentElement.getAttribute("cls-time"));
                        for(let i of not_study_idx){
                            li.parentElement.parentElement.querySelector(`div.innerText[value='${Number(i)+1}']`).innerText = `야자`;//cls['class_name'];
                        }
                        li.parentElement.parentElement.querySelector(`div.innerText[value='${Number(idx)+1}']`).innerText = `${cls['class_type']} (${cls['class_location']})`;//cls['class_name'];
                        day.setAttribute("cls-ids", req);
                    } else {
                        alert("실패, 재시도 요망");
                    }

                    loading(false);
                    
                    page.querySelector("img.btn-close[aria-label='Close'].select").click();
                })
            }

        })
    }
}

/**
 * 왼쪽 화살표 누르면 일주일 전의 한 주 일정을 불러옴
 * 단 3월 전의 일정은 안 됨.
 */
dlarrow.addEventListener("click", async (e) => {
    console.log("aaa");
    e.target.setAttribute("disable", true);
    present.setDate(present.getDate()-7);
    let diff = diffDate(present, new Date());

    if(diffDate(present, new Date(`${present.getFullYear()}-03-01`)) < 0){
        present.setDate(present.getDate()+7);
        console.log("학기 중까지만 가능.");
        return;
    }

    if(diff >= 0){
        for(let inp of page.querySelector("div.content.mainCover").querySelectorAll("div.input")){
            inp.classList.remove("disabled");
        }
    } else {
        for(let inp of page.querySelector("div.content.mainCover").querySelectorAll("div.input")){
            inp.classList.add("disabled");
        }
    }

    await weekSetter(new Date(present));
    e.target.setAttribute("disable", false);
})

/**
 * 오른쪽 화살표 누르면 일주일 후의 한 주 일정을 불러옴
 * 단 3주 이상은 안 됨.
 */
drarrow.addEventListener("click", async (e) => {
    console.log("aaa");
    e.target.setAttribute("disable", true);
    present.setDate(present.getDate()+7);
    let diff = diffDate(present, new Date());

    if(diff > 21){
        present.setDate(present.getDate()-7);
        console.log("3주 까지만 가능");
        return;
    }

    if(diff >= 0){
        for(let inp of page.querySelector("div.content.mainCover").querySelectorAll("div.input")){
            inp.classList.remove("disabled");
        }
    } else {
        for(let inp of page.querySelector("div.content.mainCover").querySelectorAll("div.input")){
            inp.classList.add("disabled");
        }
    }

    await weekSetter(new Date(present));
    e.target.setAttribute("disable", false);
})

/**
 * 자동 기입 서비스를 클릭하면 발생하는 이벤트
 * 각각 신청한 걸 result에 저장해서 보내줌
 * 아까랑 같이 첫째걸 클릭하면 조퇴, 둘째는 야자, 셋째는 선택한 것의 id가 저장됨
 */
autowrite.addEventListener("click", () => {
    let result = {
        session: session,
        mon_fixed: user_inform['mon_fixed'],
        tue_fixed: user_inform['tue_fixed'],
        wed_fixed: user_inform['wed_fixed'],
        thr_fixed: user_inform['thr_fixed'],
    };

    let clss = {
        mon_fixed: user_inform["mon_fixed"].split("/"),
        tue_fixed: user_inform["tue_fixed"].split("/"),
        wed_fixed: user_inform["wed_fixed"].split("/"),
        thr_fixed: user_inform["thr_fixed"].split("/"),
    }

    const autoSecond = page.querySelector("div.modal-content.autoSecond");

    for(let d of fixed_days_list){
        let fixed_day = fixed_days[d];
        let cls = clss[d];
        for(let idx of [0, 1, 2]){
            let fixed_day_inp = fixed_day.querySelector(`div.innerText[value="${idx+1}"]`);
            if(cls[idx] == "0"){
                fixed_day_inp.innerText = "야자";
            } else if(cls[idx] == "1"){
                fixed_day_inp.innerText = "조퇴";
            } else if(cls[idx] == "-1"){
                fixed_day_inp.innerText = "외출";
            } else{
                fixed_day_inp.innerText = `${all_lesson_byid[cls[idx]]['class_type']} (${all_lesson_byid[cls[idx]]['class_location']})`;
            }

            let temp_ul = fixed_day.querySelector(`ul[cls-time='${idx}']`);
            
            for(let li of temp_ul.querySelectorAll(`li[value='1']`)){
                li.addEventListener("click", () => {
                    for(let i of [0, 1, 2]){
                        fixed_day.querySelector(`div.innerText[value="${i+1}"]`).innerText = "조퇴";
                        cls[i] = "1";
                    }
                    result[d] = cls.join("/");
                });
            }
            
            for(let li of temp_ul.querySelectorAll(`li[value='2']`)){
                li.addEventListener("click", () => {
                    for(let i of [0, 1, 2]){
                        fixed_day.querySelector(`div.innerText[value="${i+1}"]`).innerText = "외출";
                        cls[i] = "-1";
                    }
                    result[d] = cls.join("/");
                });
            }
    
            for(let li of temp_ul.querySelectorAll("li[value='3']")){
                li.addEventListener("click", () => {
                    for(let i of [0, 1, 2]){
                        let tmp = fixed_day.querySelector(`div.innerText[value="${i+1}"]`);
                        if(tmp.innerText == "조퇴" || tmp.innerText == "외출"){
                            tmp.innerText = "야자";
                            cls[i] = "0";
                        }
                    }
                    fixed_day_inp.innerText = "야자";
                    cls[idx] = "0"
                    result[d] = cls.join("/");
                });
            }
    
            for(let li of temp_ul.querySelectorAll("li[value='4']")){
                li.addEventListener("click", () => {
                    autoSecond.style = "display: flex;"
                    modal.style = "display: none;"
    
                    autoSecond.querySelector("div.order.scheduleList.auto").innerHTML = "";
                    autoSecond.querySelector("div.afterschool.scheduleList.auto").innerHTML = "";
                    autoSecond.querySelector("h5.auto.modal-title").innerText = li.parentElement.parentElement.querySelector("div.weekday").innerText + " 주문형 / 방과후 선택";
                    let classes = undefined;
                    if(d == "mon_fixed"){
                        classes = all_lesson['mon'][idx];
                    } else if(d == "tue_fixed"){
                        classes = all_lesson['tue'][idx];
                    } else if(d == "wed_fixed"){
                        classes = all_lesson['wed'][idx];
                    } else if(d == "thr_fixed"){
                        classes = all_lesson['thr'][idx];
                    }
            
                    for(let clas of classes){
                        let cp = list.cloneNode();
                        cp.id = clas['id'];
                        cp.innerText = `${clas['class_location']} : ${clas['teacher']} ${clas['class_name']}`;
                        if(clas['class_type'] == "주문형"){
                            autoSecond.querySelector("div.order.scheduleList.auto").appendChild(cp);
                        } else if(clas['class_type'] == "방과후"){
                            autoSecond.querySelector("div.afterschool.scheduleList.auto").appendChild(cp);
                        }
    
                        cp.addEventListener("click", () => {
                            fixed_day_inp.innerText = `${clas['class_type']} (${clas['class_location']})`;//cls['class_name'];
                            cls[idx] = cp.id;
                            result[d] = cls.join("/");
    
                            modal.style = "display: flex;"
                            autoSecond.style = "display: none;"
                        });
    
                        autoSecond.querySelector("div.modal-header.auto > img").addEventListener("click", () => {
                            modal.style = "display: flex;"
                            autoSecond.style = "display: none;"
                        })
                    }
                });
            }
        }
    }

    modal.querySelector("div.modal-footer > img.autoWriteConfirm").addEventListener("click", async () => {
        loading(true);
        
        let server_result = await postFetch(JSON.stringify(result), base + "afterschool/fix", "application/json")
        .then(async res => await res.json());

        console.log(server_result);

        if(server_result['result']){
            alert("성공했습니다.");
            for(let dd of fixed_days_list){
                user_inform[dd] = result[dd];
            }
            modal.querySelector("div.modal-header.auto > img").click();
        } else{
            alert("전송 실패, 재시도 요망");
        }

        loading(false);
    })
})

loading(false);