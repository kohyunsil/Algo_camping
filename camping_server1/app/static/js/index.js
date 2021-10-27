var count = 0;
var items = [];
var tag_arrs = [];
var maxTags = 3;
const SWIPER_RECOMMEND = 5;
const SWIPER_BANNER = 3;
var x, y;

var val = document.cookie.split(';');
var param = {
    access_token: ''
};
try{
    for (var i = 0; i < val.length; i++) {
        x = val[i].substr(0, val[i].indexOf('='));
        y = val[i].substr(val[i].indexOf('=') + 1);
        x = x.replace(/^\s+|\s+$/g, ''); // 앞과 뒤의 공백 제거하기
        if (x == 'access_token') {
          param.access_token = unescape(y); // unescape로 디코딩 후 값 리턴
        }
    }
}catch (e){
    param.access_token = ''
}

// 새로고침
if (performance.navigation.type == 1 && (param.access_token !== '' || param.access_token !== undefined)){
        $.getJSON('/main/swiper/recommend/1', param).done(function(response){
            if (response.code === 200){
                // 비회원
                if (param.access_token === undefined || param.access_token === 'undefined' || param.access_token === ''){
                    $('.signin-hello-user').text(response.copy[0]);
                    GetRecommendBanner.showRecommendBanner(response);
                }else{
                    // 회원
                    $('.signin-hello-user').text(response.name + '님, ' + response.copy[0]);
                    GetRecommendBanner.showRecommendBanner(response);
                }
            }
        })

}else{
    // 새로고침 x
    $.getJSON('/main/swiper/recommend/0', param).done(function(response){
        if (response.code === 200){
            // 비회원
            if (param.access_token === undefined || param.access_token === 'undefined' || param.access_token === ''){
                $('.signin-hello-user').text(response.copy[0]);
                GetRecommendBanner.showRecommendBanner(response);
            }else{
                // 회원
                $('.signin-hello-user').text(response.copy);
                GetRecommendBanner.showRecommendBanner(response);
            }
        }
    })
}
// 롤링 배너 클릭
$('.img-1').click(function(){
    var scene_no = $(this).attr('id');
    location.href= '/search/banner/' + scene_no;
})

var GetRecommendBanner = {
    showRecommendBanner: function(response){
        for (var i=0; i<SWIPER_RECOMMEND; i++){
            $('.swiper-wrapper2').append(
                '<div class="swiper-slide mySwiper2-slide" id="recommend-swiper-01">\n' +
                '   <div class="card swiper2-card-1">\n' +
                '      <img class="swiper2-img" alt="..." src=' + response.first_image[i] + '>\n' +
                '      <div class="card-body">\n' +
                '         <h6>' + response.place_name[i] + '</h6>\n' +
                '      </div>\n' +
                '   </div>\n' +
                '</div>'
            );
            swiper.update();
        }
    },
    showSwiperBanner: function(){
        $.getJSON('/main/swiper/banner').done(function(response){
            if (response.code === 200){
                for (var i=0; i<SWIPER_BANNER; i++){
                    $('.swiper-wrapper1').append(
                        '<div className="swiper-slide swiper-slide-1" id="banner-swiper-01">\n' +
                            '<div className="col-7">\n' +
                                '<img className="img-1" alt="img" src=' + response.first_image[i] + '>\n' +
                            '</div>\n' +
                            '<div className="col-5 promotion-1">\n' +
                                '<p className="h4 fw-bolder text-white promotion-title-1">' + response.copy[i] + '</p>\n' +
                            '</div>\n' +
                        '</div>\n'
                    );
                }
            }else{
                alert('다시 시도해주세요.');
            }
        })
    }
}
var MyPageEvent = {
    moveMyPage: function(){
        $('#mypage-btn').on('click', function() {
            var url = '/mypage';
            location.href = url;
        })
    }
}
var SignoutEvent = {
    doSignout: function(){
        $('#logout-btn').on('click', function() {
            // sns 로그인인 경우
            // if(SignoutEvent.getCookie('access_token') === undefined){
            //     // kakao
            //     if (Kakao.Auth.getAccessToken()) {
            //       Kakao.API.request({
            //         url: '/v1/user/unlink',
            //         success: function (response) {
            //             var url = '/auth/sns/signout';
            //             location.href = url;
            //         },
            //         fail: function (error) {
            //           console.log(error)
            //         },
            //       })
            //       Kakao.Auth.setAccessToken(undefined)
            //     }else{
            //         // naver
            //         var testPopUp;
            //         function openPopUp(){
            //             testPopUp= window.open("https://nid.naver.com/nidlogin.logout", "_blank", "toolbar=yes,scrollbars=yes,resizable=yes,width=1,height=1");
            //         }
            //         function closePopUp(){
            //             testPopUp.close();
            //         }
            //         openPopUp();
            //         setTimeout(function() {
            //             closePopUp();
            //         }, 10);
            //         var url = '/auth/sns/signout';
            //         location.href = url;
            //     }
            // }

            SignoutEvent.deleteCookie('access_token');
            console.log(SignoutEvent.getCookie('access_token'));
            var url = '/auth/signout';
            location.href = url;
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
        cnt += $('.badge-info').length;
        // 지역 선택
        $('#area-menu li a').on('click', function() {
            $('#area-default-menu').text($(this).text());
            $("#area-default-menu").val($(this).text());
        });
        // 추천 태그 선택
        $('#recommend-tag-menu li div div button').on('click', function(){
            var tag = $(this).attr('id');
            var span_tag = '<span class="badge badge-info">' + tag + '</span>'
            if (count === 0){
                $('.bootstrap-tagsinput').empty();
            }
            if (count >= maxTags){
                $('#alert-form').addClass('show');
                $('#alert-form').show();
                $('header').append(
                  ' <div class="alert alert-warning alert-dismissible fade" id="alert-form" style="display:none;" role="alert">\n' +
                    '<strong>🙋🏻‍♀️</strong> 최대 3개의 태그까지 입력할 수 있습니다.\n' +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\n' +
                  '</div>'
                );
                return;
            }else{
                if (tag_arrs.includes(tag)){
                    $('#alert-form').addClass('show');
                    $('#alert-form').show();
                    $('header').append(
                      ' <div class="alert alert-warning alert-dismissible fade" id="alert-form" style="display:none;" role="alert">\n' +
                        '<strong>🙋🏻‍♀️</strong> 이미 선택된 태그입니다.\n' +
                        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\n' +
                      '</div>'
                    );
                    return;
                }
                $('.bootstrap-tagsinput').append(span_tag);
                tag_arrs.push(tag);
                count ++;
            }
        })
    },
    // 사용자 입력 키워드
    getKeywords: function(){
        var arr = [];
        var req = '';

        // 선택된 지역
        req += '#' + $(".btn-area").text().trim();
        if (req === '#'){
            req += '지역';
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
var ClickBannerEvent = {
    clickRecommendSwiper : function(){
        $('.mySwiper2-slide').on('click', function(){
            alert('click..!');
            var click_id = $(this).attr('id');
            var access_token = SignoutEvent.getCookie('access_token');
            if (access_token === undefined){
                access_token = '';
            }
            var param = {
                id : click_id,
                access_token : access_token
            }
            $.getJSON('/main/swiper/list', param).done(function(response){
                if(response.code === 200){
                    // 임시
                    location.href = '/signin';
                }else{
                    alert(response.msg);
                }
            });
        })
    },
    clickBannerSwiper: function(){
        $('.swiper-slide-1').on('click', function(){
            var click_id = $(this).attr('id');
            var access_token = SignoutEvent.getCookie('access_token');
            if (access_token === undefined){
                access_token = '';
            }
            var param = {
                id : click_id,
                access_token : access_token
            }
            $.getJSON('/main/swiper', param).done(function(response){
                if(response.code === 200){
                    // 임시
                    location.href = '/signin';
                }else{
                    alert(response.msg);
                }
            });
        })
    }
}

var swiper = new Swiper(".mySwiper2", {
    slidesPerView: 5,
    spaceBetween: 3,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    breakpoints: {
      // 320px ~
      320: {
        slidesPerView: 2,
        spaceBetween: 20
      },
      // 480px ~
      480: {
        slidesPerView: 3,
        spaceBetween: 20
      },
      // 640px ~
      640: {
        slidesPerView: 4,
        spaceBetween: 0
      }
    }
});

MyPageEvent.moveMyPage();
SignoutEvent.doSignout();
SearchTags.getSearchTags();
SearchTags.getKeywords();
SearchTags.doSearchTags();
ClickBannerEvent.clickRecommendSwiper();
ClickBannerEvent.clickBannerSwiper();