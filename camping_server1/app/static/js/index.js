// 카테고리 체크 값 확인
var items = []

$(function(){
    var cnt = 0
    $('.outer-1').append(
        ' <div class="alert alert-warning alert-dismissible fade" id="alert-form" style="display:none;" role="alert">\n' +
            '<strong>🙋🏻‍♀️</strong> 최대 3개의 태그까지 입력할 수 있습니다.\n' +
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\n' +
        '</div>'
    );
    $('input:checkbox').on('change', function(){
        // 검색창에서 추가한 태그 개수 포함 처리
        if (cnt > 1){
            $('#alert-form').addClass('show');
            $('#alert-form').show();
            // 3개 이상 선택한 경우 비활성화
            $('input:not(:checked)').attr('disabled', 'disabled');
        }
        if ($(this).prop('checked')) {
            items.push('#' + $(this).val());
            cnt += 1
        }else {
            // 3개 이하일시 비활성화 해제
            $('input:not(:checked)').removeAttr('disabled');
            var compare = items.indexOf($(this).val());
            items.splice(compare, 1);
            cnt -= 1
        }
    });
    cnt += $('.badge-info').length;
    // console.log(cnt);
});

$(function(){
    // 지역 선택
    $('.dropdown-menu li a').on('click', function() {
        $('#dropdownMenuButton1:first-child').text($(this).text());
        $("#dropdownMenuButton1:first-child").val($(this).text());
    });
});

// 사용자 입력 키워드
function getKeywords() {
    var arr = [];
    var req = '';

    // 선택된 지역
    req += '#' + $(".dropdown-toggle").text().trim();
    if (req === '#'){
        req += '전체';
    }
    for (var i = 0; i < items.length; i++) {
        arr.push(items[i].split(',')[0]);
    }
    var tmp = arr.toString().split(',');

    for (var i = 0; i < tmp.length; i++) {
        req += tmp[i];
    }
    // 검색창에 유저가 태그를 추가로 입력했을 경우에 대한 추가
    if ($('.badge-info').text() != '') {
        req += $('.badge-info').text();
    }
    return req
}

// 검색 click
$('.search-btn').on('click', function(event){
    event.preventDefault();
    var url = '/search?keywords=';
    var params = {
        keywords: getKeywords().replace(/#/g, ';')
    }
    location.href = url + encodeURI(encodeURIComponent(params.keywords));
});
