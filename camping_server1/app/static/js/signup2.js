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
                    // $.post('user/signup', param).done(function(response){
                    //     if (response.code === 200){
                    //         var url = '/signin';
                    //         location.href = url;
                    //     }else{
                    //         alert('다시 시도해주세요.');
                    //     }
                    // });
                    location.href = '/signup/survey/first'
                }
            }
        })
    },
    surveyFirst: function(){
        var first_answer = '';

        $('.btn-survey1').bind('click', function(){
           if ($('.btn-survey1').not(this).prop('disabled') === true){
                $(this).css('backgroundColor', '#dbdbdb');
                $(this).css('color', '#707070');
                $('.btn-survey1').not(this).prop('disabled', false);
                first_answer = '';
           }else{
                $(this).css('backgroundColor', '#b5b5b5');
                $(this).css('color', '#393939');
                $('.btn-survey1').not(this).prop('disabled', true);
                first_answer = $(this).text();
           }
        })
        $('.btn-survey1-next').on('click', function(){
            if (first_answer === ''){
                alert('설문에 대한 응답을 선택해주세요.');
                return
            }else{
                location.href = '/signup/survey/second';
            }
        }),
        $('.btn-survey1-prev').on('click', function(){
            location.href = '/signup';
        })
    },
    surveySecond: function(){
        var second_answer = '';
        var second_sub_answer = '';

        $('.btn-survey2').bind('click', function(){
           if ($('.btn-survey2').not(this).prop('disabled') === true){
                $(this).css('backgroundColor', '#dbdbdb');
                $(this).css('color', '#707070');
                $('.btn-survey2').not(this).prop('disabled', false);
                second_answer = '';
           }else{
                $(this).css('backgroundColor', '#b5b5b5');
                $(this).css('color', '#393939');
                $('.btn-survey2').not(this).prop('disabled', true);
                second_answer = $(this).text();
           }
        }),
        $('.btn-survey2-1').bind('click', function(){
           if ($('.btn-survey2-1').not(this).prop('disabled') === true){
                $(this).css('backgroundColor', '#dbdbdb');
                $(this).css('color', '#707070');
                $('.btn-survey2-1').not(this).prop('disabled', false);
                second_sub_answer = '';
           }else{
                $(this).css('backgroundColor', '#b5b5b5');
                $(this).css('color', '#393939');
                $('.btn-survey2-1').not(this).prop('disabled', true);
                second_sub_answer = $(this).text();
           }
        }),
        $('.btn-survey2-next').on('click', function(){
            if (second_answer === '' || second_sub_answer === ''){
                alert('설문에 대한 응답을 선택해주세요.');
                return
            }else{
                location.href = '/signup/survey/third';
            }
        }),
        $('.btn-survey2-prev').on('click', function(){
            location.href = '/signup/survey/first';
        })
    },
    surveyThird: function(){
        var third_answer = '';

        // input form 포커스 여부 감지
        $('.etc-form').focus(function(){
            $('.btn-survey3').css('backgroundColor', '#dbdbdb');
            $('.btn-survey3').css('color', '#707070');
            $('.btn-survey3').not(this).prop('disabled', false);
            // // 강제 엔터키
            //  var e = jQuery.Event( "keydown", { keyCode: 13 } );
            //  $(this).trigger( e );
            third_answer = $('.etc-form').val();
        })
        // $('.etc-form').blur();
        $('.btn-survey3').bind('click', function(){
           if ($('.btn-survey3').not(this).prop('disabled') === true){
                $(this).css('backgroundColor', '#dbdbdb');
                $(this).css('color', '#707070');
                $('.btn-survey3').not(this).prop('disabled', false);
                third_answer = '';
           }
           else{
                $(this).css('backgroundColor', '#b5b5b5');
                $(this).css('color', '#393939');
                $('.btn-survey3').not(this).prop('disabled', true);
                third_answer = $(this).text();
                $('.etc-form').val('');
           }
        }),
        $('.btn-survey3-next').on('click', function(){
            if (third_answer === '' && $('.etc-form').val() === ''){
                alert('설문에 대한 응답을 선택해주세요.');
                return
            }else{
                location.href = '/signup/survey/fourth';
            }
        }),
        $('.btn-survey3-prev').on('click', function(){
            location.href = '/signup/survey/second';
        })
    },
    surveyFourth: function(){
        var fourth_answer = '';

        $('.btn-survey4').bind('click', function(){
           if ($('.btn-survey4').not(this).prop('disabled') === true){
                $(this).css('backgroundColor', '#dbdbdb');
                $(this).css('color', '#707070');
                $('.btn-survey4').not(this).prop('disabled', false);
                fourth_answer = '';
           }else{
                $(this).css('backgroundColor', '#b5b5b5');
                $(this).css('color', '#393939');
                $('.btn-survey4').not(this).prop('disabled', true);
                fourth_answer = $(this).text();
           }
        }),
        $('.btn-survey4-next').on('click', function(){
            if (fourth_answer === ''){
                alert('설문에 대한 응답을 선택해주세요.');
                return
            }else{
                location.href = '/signup/survey/fifth';
            }
        }),
        $('.btn-survey4-prev').on('click', function(){
            location.href = '/signup/survey/third';
        })
    },
    surveyFifth: function(){
        var fourth_answer = '';

        $('.btn-survey5').bind('click', function(){
           if ($('.btn-survey5').not(this).prop('disabled') === true){
                $(this).css('backgroundColor', '#dbdbdb');
                $(this).css('color', '#707070');
                $('.btn-survey5').not(this).prop('disabled', false);
                fourth_answer = '';
           }else{
                $(this).css('backgroundColor', '#b5b5b5');
                $(this).css('color', '#393939');
                $('.btn-survey5').not(this).prop('disabled', true);
                fourth_answer = $(this).text();
           }
        }),
        $('.btn-survey5-next').on('click', function(){
            if (fourth_answer === ''){
                alert('설문에 대한 응답을 선택해주세요.');
                return
            }else{
                location.href = '/signup/survey/sixth';
            }
        }),
        $('.btn-survey5-prev').on('click', function(){
            location.href = '/signup/survey/fourth';
        })
    },
    surveySixth: function(){
        $('.btn-main-router').on('click', function(){
            location.href = '/';
        })
    }
}
SignupEvent.signUp();
SignupEvent.checkEmail();
SignupEvent.surveyFirst();
SignupEvent.surveySecond();
SignupEvent.surveyThird();
SignupEvent.surveyFourth();
SignupEvent.surveyFifth();
SignupEvent.surveySixth();