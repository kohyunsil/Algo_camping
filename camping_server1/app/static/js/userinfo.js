var param = {
    id: '',
    nickname: '',
    access_token: ''
}

$('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
    var target = $(e.target).attr("href");
    console.log(target);

    if (target === '#nav-userinfo'){
        $('#nav-userlike-tab').removeAttr('style');
        $('#nav-userinfo-tab').css({'border': 'none'});
        $('#nav-userinfo-tab').css({'background-color': 'rgba(255, 255, 255, 0)'});
        $('#nav-userinfo-tab').css({'border-bottom': '2px solid #27335f'});
        $('#nav-userinfo-tab').css({'color': 'black'});

        MoveTabs.getUserInfo();
    }else if (target === '#nav-userlike'){
        $('#nav-userinfo-tab').removeAttr('style');
        $('#nav-userinfo-tab').css({'border-bottom': '1px solid #dbdbdb'});
        $('#nav-userinfo-tab').css({'color': '#989898'});

        $('#nav-userlike-tab').css({'border': 'none'});
        $('#nav-userlike-tab').css({'background-color': 'rgba(255, 255, 255, 0)'});
        $('#nav-userlike-tab').css({'border-bottom': '2px solid #27335f'});
        $('#nav-userlike-tab').css({'color': 'black'});

        MoveTabs.getUserLike();
    }
});

$('.resurvey-btn').click(function(){
    $(location).attr('href', '/signup/survey/first?id=' + param.id);
})

var GetToken = {
    getAccessToken: function () {
        var token = MoveTabs.getCookie('access_token');
        if (token !== undefined) {
            param.access_token = token;
        } else {
            param.access_token = '';
        }
    }
}

var MoveTabs = {
    getUserInfo: function(){
        GetToken.getAccessToken();
        if (param.access_token !== '') {
            // 토큰 유효성 확인
            $.post('user/validation', param).done(function(response){
                if (response.code === 200){
                    $.post('/user/profile').done(function(response){
                        if (response.code === 200){
                            param.nickname = response.nickname;
                            param.id = response.id;

                            MoveTabs.setCookie(response.id, response.nickname, 1);

                            // 이메일
                            $('#email-form').val(response.email);
                            $('#email-form').attr('disabled', true);
                            $('#check-btn').prop('disabled', true);

                            // 패스워드
                            $('#password-form').attr('placeholder', '••••'); // default
                            $('#password-check-form').attr('placeholder', '••••'); // default

                            // 이름
                            $('#name-form').val(response.name);

                            // 닉네임
                            $('#nickname-form').val(response.nickname);

                            // 생년월일
                            var year = response.birth_date.substr(0, 2);
                            var month = response.birth_date.substr(2, 2);
                            var day = response.birth_date.substr(4, 2);

                            $('#input-year').val(year);
                            $('#input-month').val(month);
                            $('#input-day').val(day);
                        }
                    })
                }else{
                    location.href = '/main';
                }
            })
        }
    },
    getUserLike: function(){
        GetToken.getAccessToken();
        if (param.access_token !== '') {
            // 토큰 유효성 확인
            $.post('user/validation', param).done(function(response){
                if (response.code === 200){
                    $.post('/user/like').done(function(response){
                        if (response.code === 200){

                            var like_param = {
                                'like': response.like,
                                'access_token': param.access_token
                            }
                            $.getJSON('/search/likelist', like_param).done(function(response){
                                if (response.code === 200){
                                    for (var i=0; i<like_param.like.split(',').length; i++){
                                        $('.like-list').append(
                                            '<div class="row">\n' +
                                                '<div class="d-grid gap-1 mx-auto col">\n' +
                                                    '<button class="btn p-1 btn-place" type="button">\n' +
                                                        '<img class="test-img" alt="..." src="' + response[like_param.like.split(',')[i]].first_image + '">\n' +
                                                        '<br>\n' +
                                                        '<span>' + response[like_param.like.split(',')[i]].place_name + '</span>\n' +
                                                        '<span class="score" id="algo-star"><span><img class="visitor-star-img" src="/main/download/visit_star.png"></span>' + response[like_param.like.split(',')[i]].star + "점" +'</span>\n' +
                                                    '</button>\n' +
                                                '</div>\n' +
                                            '</div>'
                                        );
                                    }
                                }
                            })
                        }
                    })
                }else{
                    location.href = '/main';
                }
            })
        }
    },
    setCookie: function(name, value, days) {
        var date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
    },
    getCookie: function(name){
        var x, y;
        var val = document.cookie.split(';');

        for (var i = 0; i < val.length; i++) {
            x = val[i].substr(0, val[i].indexOf('='));
            y = val[i].substr(val[i].indexOf('=') + 1);
            x = x.replace(/^\s+|\s+$/g, ''); // 앞과 뒤의 공백 제거하기
            if (x === name) {
              return unescape(y); // unescape로 디코딩 후 값 리턴
            }
        }
    }
}

var SaveUserInfo = {
    saveProfile: function(){
        $('.btn-modifiy-ok').on('click', function(){
            var param = {
                email : $('#email-form').val(),
                password : $('#password-form').val(),
                passwordConfirm : $('#password-check-form').val(),
                name : $('#name-form').val(),
                nickname : $('#nickname-form').val(),
                birthDate : $('#input-year').val().toString().substring(1, 3) + $('#input-month').val().toString() + $('#input-day').val().toString()
            }
            if (param.password === '0000' || param.passwordConfirm === '0000' || param.password === '' || param.passwordConfirm === ''){
                alert('패스워드를 입력해주세요.');
                $('#password-form').focus();
                return
            }
            if (param.password !== '' && param.passwordConfirm !== ''){
                if (param.password !== param.passwordConfirm){
                    alert('패스워드를 확인해주세요.');
                    $('#password-form').val('');
                    $('#password-form').focus();
                    $('#password-check-form').val('');
                    return
                }
            }
            $.post('user/profile/update', param).done(function(response){
                if (response.code === 200){
                    alert('수정이 완료되었습니다.');
                }else{
                    alert('다시 시도해주세요.');
                }
            })
        })
    }
}
MoveTabs.getUserInfo()
SaveUserInfo.saveProfile()