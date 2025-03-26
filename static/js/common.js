
// 모달창 열기
function OpenModal(
  title = "", //모달 타이틀
  id = "", // 고유 Id
  isConfirm = true, // 컨펌버튼 표시여부
  isCancle = true, // 취소버튼 표시여부
  confirmFn, // 컨펌 버튼에 전달할 함수
  confirmText = "확인", // 컨펌 버튼 텍스트
  cancleText = "취소", // 취소 버튼 텍스트
  closeBtn = false, // 우측상단 닫기버튼 표시여부
  size = "md", //모달 사이즈 "md" / "lg"
  response_data = null,
) {
  let contents = response_data;


  $("body").css("overflow", "hidden")
    .append(`<div class="dimmed"><div class='modal ${size}' id='${id}'>
    <div class="top">
        <h2 class="title">${title}</h2>
        ${closeBtn
        ? `<button class="close-btn" onclick="CloseModal('${id}')">닫기</button>`
        : ""
      }
    </div>
    <div class="contents">${contents}</div>
    ${isConfirm || isCancle
        ? `<div class="btn-wrap">
        ${isCancle
          ? `<button class="btn secondary md"  onclick="CloseModal()">${cancleText}</button>`
          : ""
        }
        ${isConfirm
          ? `<button class="btn primary  md" onclick='${confirmFn
            ? confirmFn
            : title === "발동 카드 정의 / 시나리오 구성"
              ? 'location.href = "/scenario/create.html"'
              : "CloseModal()"
          }'>${confirmText}</button>`
          : ""
        }</div>`
        : ""
      }
    </div></div>`);
}


//시나리오 관리 -> 개발 가이드 다운로드 테스트본 
//(취소 버튼에 함수넣으려고)
function OpenModal2(
  title = "", //모달 타이틀
  id = "", // 고유 Id
  isConfirm = true, // 컨펌버튼 표시여부
  isCancle = true, // 취소버튼 표시여부
  confirmFn, // 컨펌 버튼에 전달할 함수
  confirmText = "확인", // 컨펌 버튼 텍스트
  cancleText = "취소", // 취소 버튼 텍스트
  closeBtn = false, // 우측상단 닫기버튼 표시여부
  size = "md", //모달 사이즈 "md" / "lg"
  response_data = null,
) {
  let contents = response_data;


  $("body").css("overflow", "hidden")
    .append(`<div class="dimmed"><div class='modal ${size}' id='${id}'>
    <div class="top">
        <h2 class="title">${title}</h2>
        ${closeBtn
        ? '<button class="close-btn" onclick="CloseModal()">닫기</button>'
        : ""
      }
    </div>
    <div class="contents">${contents}</div>
    ${isConfirm || isCancle
        ? `<div class="btn-wrap">
        ${isCancle
          ? `<button class="btn secondary md"  onclick="makeImg()">${cancleText}</button>`
          : ""
        }
        ${isConfirm
          ? `<button class="btn primary  md" onclick='${confirmFn
            ? confirmFn
            : title === "발동 카드 정의 / 시나리오 구성"
              ? 'location.href = "/scenario/create.html"'
              : "CloseModal()"
          }'>${confirmText}</button>`
          : ""
        }</div>`
        : ""
      }
    </div></div>`);
}


//ESC시 Modal창 닫기
function escCloseModal() {
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      CloseModal();
    }
  });
}






// 모달창 닫기 //지우는 곳 
function CloseModal(id = undefined) {
  if (id) {
    $(`#${id}`).remove()
    $("body").css("overflow", "auto");
    $(".dimmed:last").remove();
  } else {
    $("body").css("overflow", "auto");
    $(".dimmed").remove();
  }

}

// 아코디언 토글메뉴
function AccordionMenu(name) {
  if ($(`.accordion-title[data-title='${name}']`).hasClass("on")) {
    $(`#statusText`).text("열기");
  } else {
    $(`#statusText`).text("닫기");
  }
  $(`.accordion-title[data-title='${name}']`).toggleClass("on");

  $(`.accordion-contents[data-name='${name}']`).slideToggle(200);
}

// 학습 시작관련 로직
function LearnStart() {
  let isFail = true;
  // 실패시 isFail = true;
  if (isFail) {
    OpenModal(
      "학습 실패",
      "learnFail",
      true,
      false,
      "",
      "확인",
      "",
      false,
      "md"
    );
  } else {
    console.log("학습 성공");
  }
}

//셀렉트박스 라벨 클릭시
function ClickSelectLabel(id, id2) {
  if ($(`#${id}`).next().is(":visible")) {
    $(`#${id}`).removeClass("on");
    $(`#${id}`).next().hide();
  } else {
    $(".label").removeClass("on");
    $(`.options[data-id='${id}']`).not($(".options").hide());
    $(`#${id}`).addClass("on");
    $(`#${id}`).next().show();
    //신규 카드 추가 -> 선택 항목 설정
    $(`#${id2}`).text('유형 선택');
  }
}

//셀렉트박스 옵션 클릭시 (name 부여)
function ClickSelectOption(id, option, name, name2 = undefined) {
  if (id.includes('step')) {
    $(`#${id}`).attr('data', option);
  }
  $(`#${id}`).text(option);
  $(`#${id}`).attr('name', name);
  $(`#${id}`).attr('data-id', name2);
  $(`#${id}`).removeClass("on");
  $(`#${id}`).next().hide();
}


//인풋 입력시
function ChangeInput(id) {
  if ($(`#${id}`).val().length > 0) {
    $(`#${id}`).next($(".delete-btn")).show();
  } else {
    $(`#${id}`).next($(".delete-btn")).hide();
  }
}

// 인풋 포커스시
function FocusInput(id) {
  if ($(`#${id}`).prop('tagName') == 'TEXTAREA') {
    $(`#${id}`).css("border-color", "var(--blue900)");
  }
  $(".input-wrap").css("border-color", "var(--grey250)");
  $(`#${id}`).parent().css("border-color", "var(--blue900)");
}

// 인풋 포커스 해제시
function BlurInput(id) {
  const timer = setTimeout(() => {
    if (!$(".input").is(":focus")) {
      $(`#${id}`).parent().css("border-color", "var(--grey200)");
    } else {
      $(`#${id}`).css("border-color", "var(--grey200)");
    }
    clearTimeout(timer);
  }, 10);
}

// 인풋 value 삭제버튼
function DeleteInput(id) {
  $(`#${id}`).focus();
  $(`#${id}`).val("");
  $(`#${id}`).next($(".delete-btn")).hide();
}

// NlU 인풋 기존 데이터 삭제버튼(0112영현)
function DeleteInputNlu(id) {
  $(`#${id}`).parent().parent().parent().remove()
}

// NOTE: 하위 시나리오 테이블 삭제버튼 기능 (0123영현)
function deleteScen(button) {
  $(button).closest('table').remove()
}

// 체크박스 클릭 (단일 체크만)
function ChangeCheckBox(id) {
  $(`input`).prop('checked', false)
  $(".checked").removeClass('checked');

  if (id === "allCheck") {
    if ($(`#${id}`).next().hasClass("checked")) {
      $(".checkbox-label").removeClass("checked");
    } else {
      $(".checkbox-label").addClass("checked");
    }
  } else {
    $(`#${id}`).next().toggleClass("checked");
    $(`input#${id}:input`).prop("checked", true)
  }
}

// 체크박스 (다중 체크시)
function ChangeCheckBox2(id) {
  if (id === "allCheck") {
    if ($(`#${id}`).next().hasClass("checked")) {
      $(".checkbox-label").removeClass("checked");
    } else {
      $(".checkbox-label").addClass("checked");
    }
  } else {
    if ($(`label[for="${id}"]`).hasClass('checked')) {
      $(`label[for="${id}"]`).removeClass('checked')
      $(`input#${id}:input`).prop("checked", false)
    }
    else {
      $(`#${id}`).next().toggleClass("checked");
      $(`input#${id}:input`).prop("checked", true)
    }
  }
  console.log($(`#${id}`).prop("checked"))
}

// 등록 대기 인텐트 추가
function AddIntent(titleId, contentId) {
  $(".intent-add-table").append(
    `<tr><td><em class="error">${$(
      `#${titleId}`
    ).val()}</em> <button class="btn tertiary sm" onclick="DeleteIntent('${$(
      `#${titleId}`
    ).val()}')">삭제</button></td><td>0</td></tr>`
  );
}

// 등록 대기 인텐트 삭제
function DeleteIntent(name) {
  $(".intent-add-table tr").each(function () {
    const intentName = $(this).find("em").text();
    if (intentName === name) {
      $(this).remove();
    }
  });
}

// 유사 질의어 인풋 추가
function AddQueryInput() {
  const num = $(".query-table .tbody tr").length + 1;
  $(".query-table .tbody").append(
    `
    <tr>
      <td>${num > 99 ? num : num > 9 ? `0${num}` : `00${num}`}</td>
      <td>
        <div class="input-wrap">
          <input id="query${num}" class="input" placeholder="유사 질의어 입력" onfocus="FocusInput('query${num}')" oninput="ChangeInput('query${num}')" onblur="BlurInput('query${num}')">
          <span class="delete-btn" onclick="DeleteInput('query${num}')"></span>
        </div>
      </td>
    </tr>`
  );
}

/*
NOTE: 통계 Tab 금주,금월,직접 BTN
*/

const date = new Date();
// 오늘의 요일
const today = date.getDay();
// 이번 주의 첫째 날
const diff = date.getDate() - today + (today === 0 ? -6 : 1);
const firstDayOfThisWeek = new Date(date);
firstDayOfThisWeek.setDate(diff);
// 오늘의 날짜 포맷
let today_format = date.toISOString().slice(0, 10);
// 이번 주의 첫째 날 포맷
let week_format = firstDayOfThisWeek.toISOString().slice(0, 10);
// 이번 달의 첫째 날 포맷
let month_format = new Date(date.getFullYear(), date.getMonth(), 2).toISOString().slice(0, 10);



//날짜 초기 셋팅
function setToday() {
  $("#startDay").val(today_format)
  $("#endDay").val(today_format)

  //캘린더 미래시점 금지
  $('input[type="date"]').attr('max', today_format);

  $('#endDay').on('change', function () {
    var startDate = $('#startDay').val()
    var endDate = $('#endDay').val()
    //끝날짜가 시작날짜보다 이전날이 눌리는 것을 방지
    if (endDate < startDate) {
      values = `<p>끝 날짜는 시작 날짜보다 이전일수는 없습니다.</p>`
      OpenModal('날짜 오류', "", false, false, "", "", "", true, "sm", values)
      $('#endDay').val(today_format)
    }
  });

  //다른btn에서 검색날짜만 바뀔경우
  $('#startDay').on('change', () => {
    $(".filter-btns").find("button").addClass("off")
    $("#custom").removeClass("off")
  })
}


// 날짜 변경 함수
function onbtn(button) {
  $(".filter-btns").find("button").addClass("off")
  $(button).removeClass("off")
  SearchAgin($(button).attr('id'))
}

// 날짜 선택 함수
function SearchAgin(option) {
  if (option == 'today') {
    $(".active").find("input#startDay").val(today_format)
    $(".active").find("input#endDay").val(today_format)
  } else if (option == 'week') {
    $(".active").find("input#startDay").val(week_format)
    $(".active").find("input#endDay").val(today_format)
  } else if (option == 'month') {
    $(".active").find("input#startDay").val(month_format)
    $(".active").find("input#endDay").val(today_format)
  } else if (option == 'custom') {
    $(".active").find("input#startDay").val('')
    $(".active").find("input#endDay").val('')
  }
}


/*
NOTE
통계Tab - 검색 Btn
날짜 미입력시 Modal창
*/
function DateSearchBtn() {
  $(".active").find("button#DateSearchBtn").click(() => {
    let startDay = $("#startDay").val();
    let endDay = $("#endDay").val();

    if (startDay == "" || startDay == "") {
      values = `<p>검색할 날짜를 선택해주세요.</p>`
      OpenModal('날짜 미선택', "", false, false, "", "", "", true, "sm", values)
    }
  })
}

//하단 조회시 계산하는 함수
function calculateTotal(className) {
  var temp = 0;
  $("td." + className).each(function () {
    temp += $(this).text() === "-" ? 0 : parseInt($(this).text());
  });
  return temp;
}

////////////////////////////////////통계 끝///////////////////////////////////////////////

//===========================================================

// // 유사 질의어 인풋 추가
// function AddScenarioTable() {
//   console.log("clicked");
//   const num = $(".scenario-add-table").length + 1;
//   $(".scenario-steps").append(
//     `
//     <table class="table scenario-add-table">
//       <caption>
//         시나리오 생성 테이블
//       </caption>
//       <colgroup>
//         <col width="200px" />
//         <col />
//       </colgroup>
//       <thead class="thead type3">
//         <tr>
//           <th>
//             <div class="flex align-center gap-xs">
//               <span>Step</span>
//               <div class="select-box sm">
//                 <strong
//                   class="label"
//                   onclick="ClickSelectLabel('step${num}')"
//                   id="step${num}"
//                 >
//                   ${num}
//                 </strong>
//                 <ul class="options type">
//                   <li
//                     class="option"
//                     onclick="ClickSelectOption('step${num}',${num})"
//                   >
//                   ${num}
//                   </li>
//                   <li
//                     class="option"
//                     onclick="ClickSelectOption('step${num}',${num + 1})"
//                   >
//                   ${num + 1}
//                   </li>
//                   <li
//                     class="option"
//                     onclick="ClickSelectOption('step${num}',${num + 2})"
//                   >
//                   ${num + 2}
//                   </li>
//                 </ul>
//               </div>
//             </div>
//           </th>
//           <th>단계 별 시나리오 정의</th>
//         </tr>
//       </thead>
//       <tbody class="tbody">
//         <tr>
//           <td class="grey">카드 인텐트 정의</td>
//           <td>
//             <div class="flex align-center gap-xs">
//               <div class="input-wrap">
//                 <input
//                   id="scenarioJustice${num}"
//                   class="input"
//                   placeholder="C0100 / I0000100 / 날짜직접입력"
//                   onfocus="FocusInput('scenarioJustice${num}')"
//                   oninput="ChangeInput('scenarioJustice${num}')"
//                   onblur="BlurInput('scenarioJustice${num}')"
//                 />
//                 <span
//                   class="delete-btn"
//                   onclick="DeleteInput('scenarioJustice${num}')"
//                 ></span>
//               </div>
//               <button class="btn tertiary sm" onclick="OpenModal('카드 인텐트 검색','',true,true,'','확인','취소',true,'xl')">카드 인텐트 검색</button>
//             </div>
//           </td>
//         </tr>
//         <tr>
//           <td class="grey">카드 설명</td>
//           <td>
//           <div class="input-wrap">
//           <input
//             id="scenarioExplain${num}"
//             class="input"
//             placeholder="카드 설명"
//             onfocus="FocusInput('scenarioExplain${num}')"
//             oninput="ChangeInput('scenarioExplain${num}')"
//             onblur="BlurInput('scenarioExplain${num}')"
//           />
//           <span
//             class="delete-btn"
//             onclick="DeleteInput('scenarioExplain${num}')"
//           ></span>
//         </div>
//           </td>
//         </tr>
//         <tr>
//           <td class="grey">업무 설명</td>
//           <td>
//             <div class="input-wrap">
//             <input
//               id="order_info${num}"
//               class="input"
//               placeholder="업무 설명"
//               onfocus="FocusInput('order_info${num}')"
//               oninput="ChangeInput('order_info${num}')"
//               onblur="BlurInput('order_info${num}')"
//             />
//             <span
//               class="delete-btn"
//               onclick="DeleteInput('order_info${num}')"
//             ></span>
//           </div>
//           </td>
//         </tr>
//       </tbody>
//     </table>
//     `
//   );
// }

// 유사 질의어 인풋 추가
function AddSlangInput() {
  const num = $(".slang-table .tbody tr").length + 1;
  $(".slang-table .tbody").append(
    `
    <tr>
      <td>
        <input id="idCheck${num}" type="checkbox" class="checkbox" onclick="ChangeCheckBox2('idCheck${num}')">
        <label for="idCheck${num}" class="checkbox-label checked" >체크</label>       
      </td>
      <td>
        ${num > 99 ? num : num > 9 ? `0${num}` : `00${num}`}    
      </td>
      <td class="tl">
        <div class="input-wrap">
          <input id="new_slang${num}" class="input sm" placeholder="비속어 입력" onfocus="FocusInput('slang${num}')" oninput="ChangeInput('slang${num}')" onblur="BlurInput('slang${num}')">
          <span class="delete-btn" onclick="DeleteInput('slang${num}')"></span>
        </div>
      </td>
    </tr>`
  );
  $(`#idCheck${num}`).prop("checked", true)
}

function moving(address) {
  window.location.href = address;
}


// 세션 체크시
function session_check_page(response) {
  if(typeof(response) == "number"){
    values = `<p>세션 기간 만료로 로그인페이지로 이동합니다.</p>`
    OpenModal("완료", "", true, "", `top.location.href="/"`, "확인", "", "", "sm", values)
    return;
  } 
}


//테스트용
