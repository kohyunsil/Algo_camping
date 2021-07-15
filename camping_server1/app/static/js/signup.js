var SignupEvent = {
    checkEmail: function(){
        $('#check-btn').on('click', function(){
            var email = $('#email-form').val();
            var param = {
                email : email,
                flag : ''
            }
            console.log(email);
            if (email !== ''){
                $.ajax({
                    type : 'POST',
                    contentType : 'application/json',
                    url : '/user/check',
                    dataType : 'json',
                    data : JSON.stringify(param),
                    success : function(response){
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
                    },error : function(response){
                        alert('다시 시도해주세요.' + response.code);
                        $('#email-form').focus();
                    }
                });
            }else{
                alert('이메일을 입력해주세요');
            }
        })
    },
    signUp: function(){
        $('#signin-btn').on('click', function(){
            var email = $('#email-form').val();
            var password = $('#password-form').val();
            var name = $('#name-form').val();

            var info = {
                email : email,
                password : password,
                name : name
            }
            console.log(info);
            if (email === ''){
                alert('이메일을 입력해주세요');
            }
            if (password === ''){
                alert('패스워드를 입력해주세요');
            }
            if (name === ''){
                alert('이름을 입력해주세요');
            }
            if (password !== '' && name !== '' && email !== ''){
                if ($('#check-btn').is(':disabled')){
                    $.ajax({
                        type : 'POST',
                        contentType : 'application/json',
                        url : '/user/signup',
                        dataType : 'json',
                        data : JSON.stringify(info),
                        success : function(response){
                            if (response.code === 200){
                                var url = '/signin';
                                location.href = url;
                            }else{
                                alert('다시 시도해주세요.');
                            }
                        },error : function(response){
                            alert('다시 시도해주세요.' + response.code);
                        }
                    });
                }
            }
        })
    }
}
SignupEvent.signUp();
SignupEvent.checkEmail();