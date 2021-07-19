var SigninEvent = {
    signIn: function(){
        $('#signin-btn').on('click', function(){
            var param = {
                email : $('#email-form').val(),
                password : $('#password-form').val()
            }
            if (param.email === ''){
                alert('이메일을 입력해주세요.');
            }
            if (param.password === ''){
                alert('패스워드를 입력해주세요.');
            }
            if (param.email !== '' && param.password !== ''){
                $.post('/user/signin', param).done(function(response){
                    if (response.code === 200){
                        if (response.error_msg !== ''){
                            alert(response.error_msg);
                        }else{
                            SigninEvent.setCookie('access_token', response.access_token, 1);
                            var access_token = SigninEvent.getCookie('access_token');

                            // $.ajax({
                            //     type : 'GET',
                            //     url : '/',
                            //     headers : {
                            //         Authorization : 'Bearer ' + access_token
                            //     },
                            //     data : {'email': param.email},
                            //     dataType : 'json',
                            //     success : function(response, status, xhr){
                            //         window.location.href = '/';
                            //     },
                            //     error : function(xhr, status, error){
                            //         alert(error);
                            //     }
                            // })
                        }
                    }else{
                        alert(response.code + '다시 시도해주세요.');
                    }
                })
            }
        })
    },
    kakaoSignIn: function(){
        $('.btn-kakao').on('click', function(){
            Kakao.Auth.login({
                success: function(response){
                    Kakao.API.request({
                        url: '/v2/user/me',
                        success: function(response){
                            if (response.properties !== undefined){
                                var param = {
                                    id: response.id,
                                    nickname: response.properties.nickname,
                                    kakao_account: response.kakao_account
                                }
                                console.log(param);
                                $.post('/user/sns/signin', param).done(function(response){
                                    if (response.code === 200){
                                        location.href = '/';
                                    }
                                })
                            }else{
                                alert('다시 시도해주세요.');
                            }
                        },
                        fail: function(error){
                            console.log(error);
                        }
                    })
                },
                fail: function(error){
                    console.log(error);
                }
            })
        })
    },
    setCookie(name, value, days){
        var expireDate = new Date();
        expireDate.setDate(expireDate.getDate() + days);

        var cookie_value = escape(value) + ((days == null) ? '' : '; expires=' + expireDate.toUTCString());
        document.cookie = name + '=' + cookie_value;
    },
    getCookie(name){
        var x, y;
        var val = document.cookie.split(';');

        for (var i = 0; i < val.length; i++) {
            x = val[i].substr(0, val[i].indexOf('='));
            y = val[i].substr(val[i].indexOf('=') + 1);
            x = x.replace(/^\s+|\s+$/g, ''); // 앞과 뒤의 공백 제거하기
            if (x == name) {
              return unescape(y); // unescape로 디코딩 후 값 리턴
            }
        }
    }
}
SigninEvent.signIn();
SigninEvent.kakaoSignIn();