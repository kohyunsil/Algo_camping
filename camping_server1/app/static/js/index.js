// 카테고리 체크 값 확인
var items = []
var SignoutEvent = {
    doSignout: function(){
        $('#logout-btn').on('click', function() {
            // sns 로그인인 경우
            if(SignoutEvent.getCookie('access_token') === undefined){
                if (Kakao.Auth.getAccessToken()) {
                  Kakao.API.request({
                    url: '/v1/user/unlink',
                    success: function (response) {
                        var url = '/user/sns/signout';
                        location.href = url;
                    },
                    fail: function (error) {
                      console.log(error)
                    },
                  })
                  Kakao.Auth.setAccessToken(undefined)
                }
            }else{
                SignoutEvent.deleteCookie('access_token');
                var url = '/user/signout';
                location.href = url;
            }
        })
    },
    deleteCookie: function(name) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;';
    },
    getCookie: function(name){
        var x, y;
        var val = document.cookie.split(';');

        try{
            for (var i = 0; i < val.length; i++) {
                x = val[i].substr(0, val[i].indexOf('='));
                y = val[i].substr(val[i].indexOf('=') + 1);
                x = x.replace(/^\s+|\s+$/g, ''); // 앞과 뒤의 공백 제거하기
                if (x == name) {
                  return unescape(y); // unescape로 디코딩 후 값 리턴
                }
            }
        }catch (e){
            return null
        }
    }
}

var SearchTags = {
    getSearchTags: function(){
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
        // 지역 선택
        $('.dropdown-menu li a').on('click', function() {
            $('#default-menu').text($(this).text());
            $("#default-menu").val($(this).text());
        });
    },
    // 사용자 입력 키워드
    getKeywords: function(){
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
    },
    doSearchTags: function(){
        // 검색 click
        $('.search-btn').on('click', function(event){
            event.preventDefault();
            var url = '/search?keywords=';
            var params = {
                keywords: getKeywords().replace(/#/g, ';')
            }
            location.href = url + encodeURI(encodeURIComponent(params.keywords));
        });
    }
}
SignoutEvent.doSignout();
SearchTags.getSearchTags();
SearchTags.getKeywords();
SearchTags.doSearchTags();


