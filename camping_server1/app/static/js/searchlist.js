const MAX_TAG = 3;
const LIMIT_RANGE = 16;

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
                        SearchList.getSearchData(response, row_nums);
                    }else{
                        alert(response.code);
                    }
                })
                // 인기순
                $('#btnradio-popular').click(function() {
                    $.getJSON('/search/pagination/popular/' + row_nums + '/' + page, params).done(function (response) {
                        if (response.code === 200) {
                            SearchList.getSearchData(response, row_nums);
                        } else {
                            alert(response.code);
                        }
                    });
                })

                // 등록순
                $('#btnradio-update').click(function() {
                    $.getJSON('/search/pagination/recent/' + row_nums + '/' + page, params).done(function (response) {
                        if(response.code === 200){
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
    // 검색결과 정렬
    sortList: function(){
        // 인기순
        $('#btnradio-popular').click(function() {
            $.getJSON('/search/pagination/popular/' + total_row + '/' + 1, params).done(function(response){
                if(response.code === 200){
                    SearchList.getSearchData(response);
                }else{
                    alert(response.code);
                }
        });
        // 등록순
        $('#btnradio-update').click(function() {
                $.getJSON('/search/pagination/recent/' + total_row + '/' + 1, params).done(function (response) {
                    if(response.code === 200){
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
                var row_nums = response.row_nums;
                total_row = row_nums;

                $.getJSON('/search/pagination/list/' + response.row_nums + '/' + 1, params).done(function(response){
                    if(response.code === 200){
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
        var rtn_keywords = '';
        rtn_keywords = res.keywords;

        try{
            $('#area-default-menu').text(rtn_keywords.substr(0, 2));
            $("#area-default-menu").val(rtn_keywords.substr(0, 2));
        } catch(err){

        }
        $('.input-keyword').text(rtn_keywords);
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
                    '<p class="card-text">95% 일치</p>'
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
SearchList.sortList()
SearchList.getList()