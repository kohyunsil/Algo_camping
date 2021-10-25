const MAX_TAG = 3;
const LIMIT_RANGE = 16;
// header logo img 경로
$('.header-logo-img').attr('src', '/static/imgs/algo_logo2.png');

var params = {
    keywords : ''
}
var total_row = 0;
var Pagination = {
    // 페이지 수 처리
    pageList: function(row_nums){
        $('#pagination').twbsPagination({
            totalPages: row_nums / LIMIT_RANGE,
            visiblePages: 5,
            startPage: 1,
            initiateStartPageClick: false,
            first: '<<',
            prev: false,
            next: false,
            last: '>>',
            lastClass: 'page-item last',
            firstClass: 'page-item first',
            pageClass: 'page-item',
            activeClass: 'active',
            disabledClass: 'disabled',
            anchorClass: 'page-link',

            onPageClick: function (event, page) {
                // 다음 페이지 클릭 처리
                $.getJSON('/search/pagination/list/' + row_nums + '/' + page, params).done(function(response){
                    if(response.code === 200){
                        var regex = / /gi;
                        var keyword_arrs = params.keywords.replace(regex, '').trim().split(';');
                        $('.bootstrap-tagsinput').empty();

                        for (var i=2; i<keyword_arrs.length; i++){
                            var span_tag = '<span class="badge badge-info">' + keyword_arrs[i] + '</span>'
                            $('.bootstrap-tagsinput').append(span_tag);
                        }
                        SearchList.getSearchData(response, row_nums);
                    }else{
                        alert(response.code);
                    }
                })
                // 인기순
                $('#btnradio-popular').click(function() {
                    $.getJSON('/search/pagination/popular/' + row_nums + '/' + page, params).done(function (response) {
                        if (response.code === 200){
                            var regex = / /gi;
                            var keyword_arrs = params.keywords.replace(regex, '').trim().split(';');
                            $('.bootstrap-tagsinput').empty();

                            for (var i=2; i<keyword_arrs.length; i++){
                                var span_tag = '<span class="badge badge-info">' + keyword_arrs[i] + '</span>'
                                $('.bootstrap-tagsinput').append(span_tag);
                            }
                            SearchList.getSearchData(response, row_nums);
                        }else{
                            alert(response.code);
                        }
                    });
                })
                // 등록순
                $('#btnradio-update').click(function() {
                    $.getJSON('/search/pagination/recent/' + row_nums + '/' + page, params).done(function (response) {
                        if(response.code === 200){
                            var regex = / /gi;
                            var keyword_arrs = params.keywords.replace(regex, '').trim().split(';');
                            $('.bootstrap-tagsinput').empty();

                            for (var i=2; i<keyword_arrs.length; i++){
                                var span_tag = '<span class="badge badge-info">' + keyword_arrs[i] + '</span>'
                                $('.bootstrap-tagsinput').append(span_tag);
                            }
                            SearchList.getSearchData(response);
                        }else{
                            alert(response.code);
                        }
                    })
                })
                // 조회순
                $('#btnradio-readcount').click(function() {
                    $.getJSON('/search/pagination/readcount/' + row_nums + '/' + page, params).done(function(response){
                        if(response.code === 200){
                            SearchList.getSearchData(response);
                        }else{
                            alert(response.code);
                        }
                    })
                });
            }
        });
    }
}
var SearchList = {
    // 배너 클릭 검색 결과 (매칭도, 롤링 썸네일, 정렬 미지원)
    bannerList: function(){
        // 배너 검색 결과 여부 확인
        if (window.location.pathname.split('/')[1] === 'search' && window.location.pathname.split('/')[2] === 'banner'){
            var param = {
                scene_no: window.location.pathname.split('/')[3]
            }
            $.getJSON('/search/banner/list', param).done(function(response){
                if (response.code === 200){
                    $('.loading-bar').css({'visibility': 'hidden'});
                    $('.sort').css({'display': 'none'});

                    $('.input-keyword').text(response.copy + '에 대한');
                    $('.input-size').text(response.algostar.length);
                    $('.input-size').text(response.algostar.length);
                    $('.search-result').css({'visibility': 'visible'});
                    $('.pagination').css({'visibility': 'visible'});

                    for(var i=0; i<response.algostar.length; i++){
                        $('#card-layout').append(
                            '<div class="col" style="cursor: pointer;" name="' + response.place_info[i].content_id + '" id=' + '"' + i + '"' + '>\n' +
                                '<div class="card border-0" id="' + response.place_info[i].content_id + '" >\n' +
                                    '<div class="swiper-container card mySwiper">\n' +
                                        '<div class="swiper-wrapper" id="swiper'+ (i+1) + '">\n' +
                                            '<div class="swiper-slide">\n' +
                                                '<img class="lazy-load card-img-fluid" alt="..." src="' + response.place_info[i].first_image + '" onError="this.onerror=null;this.src=\'/static/imgs/error_logo.png\';"' +'>\n' +
                                            '</div>\n' +
                                        '</div>\n' +
                                    '</div>\n' +
                                    '<div class="card-body">\n' +
                                        '<div id="item-title' + (i+1) + '">\n'+
                                            '<a class="h5 card-title fw-bolder" href="#">'+ response.place_info[i].place_name +'</a>\n' +
                                        '</div><br>\n' +
                                        '<div class="col justify-content-md-center tags" id="tag' + (i+1) + '">\n' +
                                        '</div>&nbsp;\n' +
                                        '<p class="algo-text">\n' +
                                            '<span class="star" id="algo-star' + (i+1) + '"></span> \n' +
                                        '</p> \n' +
                                    '</div> \n' +
                                '</div> \n' +
                                '<br><br> \n' +
                            '</div> \n'
                        );
                    }
                    var star = '';
                    for (var i=0; i<response.algostar.length; i++){
                        for (var j=0; j<parseInt(response.algostar[i]); j++){
                            star += '★';
                        }
                        for (var j=0; j<(5 - parseInt(response.algostar[i])); j++){
                            star += '☆';
                        }
                        $('#algo-star' + (i+1)).text(star);
                        $('#algo-star' + (i+1)).append(
                            '<span class="detail-score">' + ' ' + response.algostar[i] + '</span>'
                        )
                        star = '';
                    }
                    // 장소 클릭
                    $('.col').each(function(idx){
                        $(this).click(function(event){
                            var idx = $(this).attr('id');
                            var content_id = $(this).attr('name');

                            location.href = '/detail/' + content_id + '/' + idx;
                        })
                    })
                }else{
                    alert('다시 시도해주세요');
                }
            })
        }
    },
    // 검색결과 정렬
    sortList: function(){
        // 인기순
        $('#btnradio-popular').click(function() {
            $.getJSON('/search/pagination/popular/' + total_row + '/' + 1, params).done(function(response){
                if(response.code === 200){
                    var regex = / /gi;
                    var keyword_arrs = params.keywords.replace(regex, '').trim().split(';');
                    var keyword_str = '';
                    $('.bootstrap-tagsinput').empty();

                    // 로그인 o인 경우 매칭도 노출
                    if (SearchList.getCookie('access_token') !== undefined){
                        for (var i=0; i<response.place_info.length; i++){
                            $('#item-title'+ (i+1)).append(
                                '<p class="card-text">' + response.match_pct[i] + "\% 일치" + '</p>'
                            )
                        }
                    }
                    for (var i=2; i<keyword_arrs.length; i++){
                        var span_tag = '<span class="badge badge-info">' + keyword_arrs[i] + '</span>'
                        $('.bootstrap-tagsinput').append(span_tag);
                    }
                    SearchList.getSearchData(response);
                }else{
                    alert(response.code);
                }
        });
        // 등록순
        $('#btnradio-update').click(function() {
                $.getJSON('/search/pagination/recent/' + total_row + '/' + 1, params).done(function (response) {
                    if(response.code === 200){
                        var regex = / /gi;
                        var keyword_arrs = params.keywords.replace(regex, '').trim().split(';');
                        $('.bootstrap-tagsinput').empty();

                        // 로그인 o인 경우 매칭도 노출
                        if (SearchList.getCookie('access_token') !== undefined){
                            for (var i=0; i<response.place_info.length; i++){
                                $('#item-title'+ (i+1)).append(
                                    '<p class="card-text">' + response.match_pct[i] + "\% 일치" + '</p>'
                                )
                            }
                        }
                        for (var i=2; i<keyword_arrs.length; i++){
                            var span_tag = '<span class="badge badge-info">' + keyword_arrs[i] + '</span>'
                            $('.bootstrap-tagsinput').append(span_tag);
                        }
                        SearchList.getSearchData(response);
                    }else{
                        alert(response.code);
                    }
                })
            })
        });
        // 조회순
        $('#btnradio-readcount').click(function() {
            $.getJSON('/search/pagination/readcount/' + total_row + '/' + 1, params).done(function(response){
                if(response.code === 200){
                    var regex = / /gi;
                    var keyword_arrs = params.keywords.replace(regex, '').trim().split(';');
                    $('.bootstrap-tagsinput').empty();

                    // 로그인 o인 경우 매칭도 노출
                    if (SearchList.getCookie('access_token') !== undefined) {
                        for (var i = 0; i < response.place_info.length; i++) {
                            $('#item-title' + (i + 1)).append(
                                '<p class="card-text">' + response.match_pct[i] + "\% 일치" + '</p>'
                            )
                        }
                    }
                    for (var i=2; i<keyword_arrs.length; i++){
                        var span_tag = '<span class="badge badge-info">' + keyword_arrs[i] + '</span>'
                        $('.bootstrap-tagsinput').append(span_tag);
                    }
                    SearchList.getSearchData(response);
                }else{
                    alert(response.code);
                }
            })
        });
    },
    // 검색결과 리스트
    getList: function(){
        var param = document.location.href.split("?keywords=");
        var decode_param = decodeURI(decodeURIComponent(param[1].toString()));
        var req_param = decode_param.replaceAll('%3B', ';').replace('추천태그', '');
        params.keywords = req_param;

        var access_token = SearchList.getCookie('access_token');

        $.getJSON('/search/list', params).done(function(response){
            if(response.code === 200){
                $('.input-keyword').text(params.keywords + '에 대한');
                var row_nums = response.row_nums;
                total_row = row_nums;

                var regex = / /gi;
                var keyword_arrs = req_param.replace(regex, '').trim().split(';');

                $('#area-default-menu').text(keyword_arrs[1]);
                $('.bootstrap-tagsinput').empty();

                for (var i=2; i<keyword_arrs.length; i++){
                    var span_tag = '<span class="badge badge-info">' + keyword_arrs[i] + '</span>'
                    $('.bootstrap-tagsinput').append(span_tag);
                }

                $.getJSON('/search/pagination/list/' + response.row_nums + '/' + 1, params).done(function(response){
                    if(response.code === 200){
                        console.log(response);
                        SearchList.getSearchData(response, row_nums);
                    }else{
                        alert(response.code);
                    }
                })
            }else{
                alert(response.code);
            }
        })
    },
    showAlgoStars: function(res){
        var star = '';

        for (var i=0; i<res.algo_star.length; i++){
            for (var j=0; j<parseInt(res.algo_star[i]); j++){
                star += '★';
            }
            for (var j=0; j<(5 - parseInt(res.algo_star[i])); j++){
                star += '☆';
            }
            $('#algo-star' + (i+1)).text(star);
            $('#algo-star' + (i+1)).append(
                '<span class="detail-score">' + ' ' + res.algo_star[i] + '</span>'
            )
            star = '';
        }
    },
    showSearchList: function(res, row_nums){
        try{
            $('#area-default-menu').text(rtn_keywords.substr(0, 2));
            $("#area-default-menu").val(rtn_keywords.substr(0, 2));
        } catch(err){

        }
        var regex = / /gi;
        var keyword_arrs = params.keywords.replace(regex, '').trim().split(';');
        var keyword_str = '';

        keyword_str += keyword_arrs[1].trim() + ', ';

        for (var i=2; i<keyword_arrs.length; i++){
            keyword_str += keyword_arrs[i].trim();

            if (i !== keyword_arrs.length -1){
                keyword_str += ', ';
            }
        }
        $('.input-keyword').text(keyword_str + '에 대한');

        if (res.flag === true){
            console.log(res.algo_star.length);
            $('.input-size').empty();
            $('.input-size').text(res.algo_star.length);
        }
        $('.input-size').text(row_nums);
        $('.search-result').css({'visibility': 'visible'});
        $('.pagination').css({'visibility': 'visible'});

        for(var i=0; i<res.place_info.length; i++){
            $('#card-layout').append(
                '<div class="col" style="cursor: pointer;" id=' + '"' + i + '"' + '>\n' +
                    '<div class="card border-0">\n' +
                        '<div class="swiper-container card mySwiper">\n' +
                            '<div class="swiper-wrapper" id="swiper'+ (i+1) + '">\n' +
                                '<div class="swiper-slide">\n' +
                                    '<img data-src="' + res.place_info[i].detail_image[0] + '" class="lazy-load card-img-fluid" alt="..."' + 'src="/static/imgs/error_logo.png" onError="this.onerror=null;this.src=\'/static/imgs/error_logo.png\';"' +'>\n' +
                                '</div>\n' +
                            '</div>\n' +
                        '</div>\n' +
                        '<div class="card-body">\n' +
                            '<div id="item-title' + (i+1) + '">\n'+
                                '<a class="h5 card-title fw-bolder" href="#">'+ res.place_info[i].place_name +'</a>\n' +
                            '</div><br>\n' +
                            '<div class="col justify-content-md-center tags" id="tag' + (i+1) + '">\n' +
                            '</div>&nbsp;\n' +
                            '<p class="algo-text">\n' +
                                '<span class="star" id="algo-star' + (i+1) + '"></span> \n' +
                            '</p> \n' +
                        '</div> \n' +
                    '</div> \n' +
                    '<br><br> \n' +
                '</div> \n'
            );
            for (var j=0; j<MAX_TAG; j++){
                if (res.tag[i].length === 0){
                    $('#tag'+ (i+1)).append(
                        '<button type="button" class="btn btn-secondary btn-sm"' + 'style="visibility:hidden;"></button>'
                    );
                }else{
                    if (res.tag[i][j] === undefined){
                        continue
                    }
                    $('#tag'+ (i+1)).append(
                    '<button type="button" class="btn btn-secondary btn-sm btn-tag">\n' +
                        res.tag[i][j] +
                    '</button>\n'
                )}
            }
        }
        // 로그인 o인 경우 매칭도 노출
        if (SearchList.getCookie('access_token') !== undefined){
            for (var i=0; i<res.place_info.length; i++){
                $('#item-title'+ (i+1)).append(
                    '<p class="card-text">' + res.match_pct[i] + "\% 일치" + '</p>'
                )
            }
        }
        // 장소 클릭
        $('.col').each(function(idx){
            $(this).click(function(event){
                var idx = $(this).attr('id');
                var id = res.place_info[idx].content_id;

                event.preventDefault();
                var param = {
                    content_id : id,
                    id : idx
                }

                location.href = '/detail/' + param.content_id + '/' + param.id;
            })
        })
    },
    showSwiperImg: function(res){
        $(this).lazyLoadXT();
        for (var i = 0; i < res.place_info.length; i++) {
            for (var k = 1; k < res.place_info[i].detail_image.length; k++) {
                $('#swiper' + (i + 1)).append(
                    '<div class="swiper-slide">\n' +
                        '<img data-src="' + res.place_info[i].detail_image[k] + '"src="/static/imgs/error_logo.png" onError="this.onerror=null;this.src=\'/static/imgs/error_logo.png\';"' + 'class="lazy-load card-img-fluid" alt="...">\n' +
                    '</div>'
                )
            }
        }
        var swiper = new Swiper(".mySwiper", {
            autoplay: {
                delay: 3500,
                disableOnInteraction: false,
            },
        });
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
    },
    getSearchData: function(response, row_nums){
        $('.loading-bar').css({'visibility': 'hidden'});
        $('.page-nav').css({'visibility': 'visible'});
        $('#card-layout').empty();
        setTimeout(function(){
            $(window).lazyLoadXT();
        }, 0);

        SearchList.showSearchList(response, row_nums);
        SearchList.showSwiperImg(response);
        SearchList.showAlgoStars(response);

        Pagination.pageList(row_nums);
    }
}

if (window.location.pathname.split('/')[2] !== 'banner') {
    SearchList.sortList()
    SearchList.getList()
}else{
    SearchList.bannerList()
}