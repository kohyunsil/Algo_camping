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
                        if (response.flag){
                            alert('존재하지 않는 회원입니다. 이메일 혹은 패스워드를 확인해주세요.');
                        }else{
                            var url = '/';
                            location.href = url;
                        }
                    }else{
                        alert(response.code + '다시 시도해주세요.');
                    }
                })
            }
        })
    }
}
SigninEvent.signIn();