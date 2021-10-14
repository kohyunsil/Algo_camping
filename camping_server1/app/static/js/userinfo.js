var param = {
    access_token: ''
}

$('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
    var target = $(e.target).attr("href");

    if (target === 'user-profile'){
        $('#nav-like-tab').removeAttr('style');

        $('#nav-profile-tab').css({'border': 'none'});
        $('#nav-profile-tab').css({'background-color': 'rgba(255, 255, 255, 0)'});
        $('#nav-profile-tab').css({'border-bottom': '2px solid #27335f'});
        $('#nav-profile-tab').css({'color': 'black'});

        MoveTabs.getUserInfo();
    }else if (target === 'user-like'){
        $('#nav-profile-tab').removeAttr('style');
        $('#nav-profile-tab').css({'border-bottom': '1px solid #dbdbdb'});
        $('#nav-profile-tab').css({'color': '#989898'});

        $('#nav-like-tab').css({'border': 'none'});
        $('#nav-like-tab').css({'background-color': 'rgba(255, 255, 255, 0)'});
        $('#nav-like-tab').css({'border-bottom': '2px solid #27335f'});
        $('#nav-like-tab').css({'color': 'black'});

        MoveTabs.getUserLike();
    }
});

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
                            $('#nav-user-profile').css({'visibility': 'visible'});
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
                            $('#nav-user-profile').css({'visibility': 'hidden'});
                            console.log('/user/like ok!');
                        }
                    })
                }else{
                    location.href = '/main';
                }
            })
        }
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