var SignupEvent = {
    checkEmail: function(){
        $('#check-btn').on('click', function(){
            var param = {
                email : $('#email-form').val(),
                flag : ''
            }
            $.post('/user/check', param).done(function(response){
                if (response.code === 200){
                    if (response.flag === false){
                        alert('사용 가능한 이메일입니다.');
                        $('#email-form').val(param.email);
                        $('#email-form').attr('disabled', true);

                        $('#check-btn').prop('disabled', true);

                    }else if (response.flag === true){
                        alert('이미 존재하는 이메일입니다.');
                        $('#email-form').val('');
                        $('#email-form').focus();
                    }
                }else{
                    alert('다시 시도해주세요.');
                    $('#email-form').focus();
                }
            })
        })
    },
    signUp: function(){
        $('#signin-btn').on('click', function(){
            var param = {
                email : $('#email-form').val(),
                password : $('#password-form').val(),
                name : $('#name-form').val()
            }
            if (param.email === ''){
                alert('이메일을 입력해주세요.');
            }
            if (param.password === ''){
                alert('패스워드를 입력해주세요.');
            }
            if (param.name === ''){
                alert('이름을 입력해주세요.');
            }
            if (param.password !== '' && param.name !== '' && param.email !== ''){
                if ($('#check-btn').is(':disabled')){
                    $.post('user/signup', param).done(function(response){
                        if (response.code === 200){
                            var url = '/signin';
                            location.href = url;
                        }else{
                            alert('다시 시도해주세요.');
                        }
                    });
                }
            }
        })
    }
}
SignupEvent.signUp();
SignupEvent.checkEmail();