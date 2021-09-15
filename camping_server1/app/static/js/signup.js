var answerParam = {
        firstAnswer: '',
        secondAnswer: '',
        secondSubAnswer: '',
        thirdAnswer: '',
        fourthAnswer: '',
        fifthAnswer: ''
}

var getQueryString = function(key){
    var str = location.href;
    var index = str.indexOf("?") + 1;
    var lastIndex = str.indexOf("#") > -1 ? str.indexOf("#") + 1 : str.length;

    // index 값이 0일때 QueryString이 없으므로 종료
    if (index == 0) {
        return "";
    }
    // str = a=1&b=first&c=true
    str = str.substring(index, lastIndex);
    str = str.split("&");

    var result = "";
    for (var i = 0; i < str.length; i++) {
        var arr = str[i].split("=");
        if (arr.length != 2) {
            break;
        }
        if (arr[0] == key) {
            result = arr[1];
            break;
        }
    }
    var decode_result = decodeURI(decodeURIComponent(result));
    // 공백 문자열 (%2C , %26) 포함 체크
    if (decode_result.indexOf('%2C') !== -1){
        decode_result = decode_result.replace('%2C', '');
    }
    if (decode_result.indexOf('%26') !== -1){
        decode_result = decode_result.replace('%26', '&');
    }
    return decode_result;
}

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
                passwordConfirm : $('#password-check-form').val(),
                name : $('#name-form').val(),
                nickname : $('#nickname-form').val()
            }
            if (param.email === ''){
                alert('이메일을 입력해주세요.');
            }
            if (param.password === ''){
                alert('패스워드를 입력해주세요.');
            }
            if (param.passwordConfirm === ''){
                alert('패스워드 확인을 입력해주세요.');
            }
            if (param.name === ''){
                alert('이름을 입력해주세요.');
            }
            if (param.nickname === ''){
                alert('닉네임을 입력해주세요.');
            }
            if (param.password !== '' && param.name !== '' && param.email !== ''){
                if ($('#check-btn').is(':disabled')){
                    if (param.password !== param.passwordConfirm){
                        alert('패스워드를 확인해주세요.');
                        $('#password-form').val('');
                        $('#password-form').focus();
                        $('#password-check-form').val('');
                        return
                    }
                    $.post('user/signup', param).done(function(response){
                        if (response.code === 200){
                            setCookie(response.id, response.nickname, 1);
                            var url = '/signup/survey/first?id=' + response.id;
                            location.href = url;
                        }else{
                            alert('다시 시도해주세요.');
                            alert(response.code);
                        }
                    });
                }
            }
        })
    },
    surveyFirst: function(){
        var first_answer = '';
        var id = getQueryString('id');

        $('.user-nickname').text(getCookie(id));
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
                answerParam.firstAnswer = first_answer;
                location.href = '/signup/survey/second?id=' + id + '&q1=' + encodeURI(encodeURIComponent(answerParam.firstAnswer));
            }
        }),
        $('.btn-survey1-prev').on('click', function(){
            location.href = '/signup';
        })
    },
    surveySecond: function(){
        var second_answer = '';
        var second_sub_answer = '';
        var id = getQueryString('id');

        $('.user-nickname').text(getCookie(id));
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
                location.href = '/signup/survey/third?id=' + id + '&q1=' + encodeURI(encodeURIComponent(getQueryString('q1'))) + '&q2=' + encodeURI(encodeURIComponent(second_answer)) +
                '&q2sub=' + encodeURI(encodeURIComponent(second_sub_answer));
            }
        }),
        $('.btn-survey2-prev').on('click', function(){
            location.href = '/signup/survey/first?id=' + id + '&q1=' + encodeURI(encodeURIComponent(getQueryString('q1')));
        })
    },
    surveyThird: function(){
        var third_answer = '';
        var id = getQueryString('id');

        $('.user-nickname').text(getCookie(id));
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
                location.href = '/signup/survey/fourth?id=' + id + '&q1=' + encodeURI(encodeURIComponent(getQueryString('q1'))) + '&q2=' + encodeURI(encodeURIComponent(getQueryString('q2'))) +
                '&q2sub=' + encodeURI(encodeURIComponent(getQueryString('q2sub'))) + '&q3=' + encodeURI(encodeURIComponent(third_answer));
            }
        }),
        $('.btn-survey3-prev').on('click', function(){
            location.href = '/signup/survey/second?id=' + id + '&q1=' + encodeURI(encodeURIComponent(getQueryString('q1'))) + '&q2=' + encodeURI(encodeURIComponent(getQueryString('q2'))) + '&q2sub='
            + encodeURI(encodeURIComponent(getQueryString('q2sub')));
        })
    },
    surveyFourth: function(){
        var fourth_answer = '';
        var id = getQueryString('id');

        $('.user-nickname').text(getCookie(id));
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
                location.href = '/signup/survey/fifth?id=' + id + '&q1=' + encodeURI(encodeURIComponent(getQueryString('q1'))) + '&q2=' + encodeURI(encodeURIComponent(getQueryString('q2'))) +
                '&q2sub=' + encodeURI(encodeURIComponent(getQueryString('q2sub'))) + '&q3=' + encodeURI(encodeURIComponent(getQueryString('q3'))) +
                '&q4=' + encodeURI(encodeURIComponent(fourth_answer));
            }
        }),
        $('.btn-survey4-prev').on('click', function(){
            location.href = '/signup/survey/third?id=' + id + '&q1=' + encodeURI(encodeURIComponent(getQueryString('q1'))) + '&q2=' + encodeURI(encodeURIComponent(getQueryString('q2'))) + '&q2sub=' +
            encodeURI(encodeURIComponent(getQueryString('q2sub'))) + '&q3=' + encodeURI(encodeURIComponent(getQueryString('q3')));
        })
    },
    surveyFifth: function(){
        var fifth_answer = '';
        var id = getQueryString('id');

        $('.user-nickname').text(getCookie(id));
        $('.btn-survey5').bind('click', function(){
           if ($('.btn-survey5').not(this).prop('disabled') === true){
                $(this).css('backgroundColor', '#dbdbdb');
                $(this).css('color', '#707070');
                $('.btn-survey5').not(this).prop('disabled', false);
                fifth_answer = '';
           }else{
                $(this).css('backgroundColor', '#b5b5b5');
                $(this).css('color', '#393939');
                $('.btn-survey5').not(this).prop('disabled', true);
                fifth_answer = $(this).text();
           }
        }),
        $('.btn-survey5-next').on('click', function(){
            if (fifth_answer === ''){
                alert('설문에 대한 응답을 선택해주세요.');
                return
            }else{
                answerParam.firstAnswer = getQueryString('q1')
                answerParam.secondAnswer = getQueryString('q2')
                answerParam.secondSubAnswer = getQueryString('q2sub')
                answerParam.thirdAnswer = getQueryString('q3')
                answerParam.fourthAnswer = getQueryString('q4')
                answerParam.fifthAnswer = fifth_answer

                // 설문 결과 전달
                $.getJSON('/user/signup/survey', answerParam).done(function(response){
                    if(response.code === 200){
                        location.href = '/signup/survey/sixth?id=' + id;
                    }else{
                        alert(response.msg);
                    }
                })
            }
        }),
        $('.btn-survey5-prev').on('click', function(){
            location.href = '/signup/survey/fourth?id=' + id + '&q1=' + encodeURI(encodeURIComponent(getQueryString('q1'))) + '&q2=' + encodeURI(encodeURIComponent(getQueryString('q2'))) +
            '&q2sub=' + encodeURI(encodeURIComponent(getQueryString('q2sub'))) + '&q3=' + encodeURI(encodeURIComponent(getQueryString('q3'))) +
            '&q4=' + encodeURI(encodeURIComponent(getQueryString('q4')));
        })
    },
    surveySixth: function(){
        var id = getQueryString('id');

        $('.user-nickname').text(getCookie(id));
        $('.btn-main-router').on('click', function(){
            location.href = '/';
        })
    }
}
var setCookie = function(name, value, days){
    var expireDate = new Date();
    expireDate.setDate(expireDate.getDate() + days);

    var cookie_value = escape(value) + ((days == null) ? '' : '; expires=' + expireDate.toUTCString());
    document.cookie = name + '=' + cookie_value;
}

var getCookie = function(name){
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

SignupEvent.signUp();
SignupEvent.checkEmail();
SignupEvent.surveyFirst();
SignupEvent.surveySecond();
SignupEvent.surveyThird();
SignupEvent.surveyFourth();
SignupEvent.surveyFifth();
SignupEvent.surveySixth();