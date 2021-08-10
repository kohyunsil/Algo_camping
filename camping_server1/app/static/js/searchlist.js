const MAX_TAG = 3;

var SearchList = {
    // 검색결과 정렬
    sortList: function(){
        // 인기순
        $('#btnradio-popular').click(function() {
            $.getJSON('/search/popular').done(function(response){
                if(response.code === 200){
                    SearchList.getSearchData(response);
                }else{
                    alert(response.msg);
                }
        });
        // 등록순
        $('#btnradio-update').click(function() {
                $.getJSON('/search/recent').done(function (response) {
                    if(response.code === 200){
                        SearchList.getSearchData(response);
                    }else{
                        alert(response.msg);
                    }
                })
            })
        });
        // 조회순
        $('#btnradio-readcount').click(function() {
            $.getJSON('/search/readcount').done(function(response){
                if(response.code === 200){
                    SearchList.getSearchData(response);
                }else{
                    alert(response.msg);
                }
            })
        });
    },
    // 검색결과 리스트
    getList: function(){
        var param = document.location.href.split("?keywords=");
        var decode_param = decodeURI(decodeURIComponent(param[1].toString()));
        var req_param = decode_param.replaceAll('%3B', ';');
        var params = {
            keywords : req_param,
            res_num : '',
            place_info : '',
        }
        var access_token = SearchList.getCookie('access_token');
        console.log(params)
        $.getJSON('/search/list', params).done(function(response){
            if(response.code === 200){
                SearchList.getSearchData(response);
            }else{
                alert(response.msg);
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
    showSearchList: function(res){
        $('.input-keyword').text(res.keywords);
        $('.input-size').text(res.res_num);
        $('.search-result').css({'visibility': 'visible'});

        for(var i=0; i<res.place_info.length; i++){
            $('#card-layout').append(
                '<div class="col" style="cursor: pointer;">\n' +
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
                event.preventDefault();
                var id = res.place_info[Number(idx / 2)].content_id;
                var param = {
                    content_id: id
                }
                var url = '/detail?content_id=';
                location.href = url + encodeURI(encodeURIComponent(param.content_id));
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
    getSearchData: function(response){
        $('.loading-bar').css({'visibility': 'hidden'});
        $('#card-layout').empty();
        setTimeout(function(){
            $(window).lazyLoadXT();
        }, 0);

        SearchList.showSearchList(response);
        SearchList.showSwiperImg(response);
        SearchList.showAlgoStars(response);
    }
}
SearchList.sortList()
SearchList.getList()