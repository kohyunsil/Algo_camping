var SignupEvent = {
    checkEmail: function(){
        $('#check-btn').on('click', function(){
            var email = $('#email-form').val();
            var param = {
                email : email
            }
            if (email !== null || email !== '' || email !== undefined){
                $.getJSON('/user/check', param).done(function(response){
                    if (response.code === 200) {
                        if (response.status === true){
                            alert('사용 가능한 이메일입니다.');
                            email.attr('check', 'success');
                            $('#check-btn').css({'background-color': 'green'});
                        }else{
                            alert('이미 존재하는 이메일입니다.');
                            $('#email-form').focus();
                            return 0;
                        }
                    }else{
                        alert('다시 시도해주세요.');
                        $('#email-form').focus();
                        return 0;
                    }
                })
            }
        })
    },
    signUp: function(){
        $('#signin-btn').on('click', function(){
            var email = $('#email-form').val();
            var password = $('#password-form').val();
            var name = $('#name-form').val();
        })
    }
}
// SignupEvent.signUp();
SignupEvent.checkEmail();