const MAX_TAG = 3;

var SearchList = {
    // 검색결과 정렬
    sortList: function(){
        // 인기순
        $('#btnradio-popular').click(function() {
            $.getJSON('/search/popular').done(function(response){
                if(response.code === 200){
                    $('#card-layout').empty();
                    setTimeout(function(){
                        $(window).lazyLoadXT();
                    }, 0);
                    SearchList.showSearchList(response);
                    SearchList.showSwiperImg(response);
                }else{
                    alert(response.msg);
                }
        });
        // 등록순
        $('#btnradio-update').click(function() {
                $.getJSON('/search/recent').done(function (response) {
                    if(response.code === 200){
                        $('#card-layout').empty();
                        setTimeout(function(){
                            $(window).lazyLoadXT();
                        }, 0);

                        SearchList.showSearchList(response);
                        SearchList.showSwiperImg(response);
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
                    $('#card-layout').empty();
                    setTimeout(function(){
                        $(window).lazyLoadXT();
                    }, 0);
                    SearchList.showSearchList(response);
                    SearchList.showSwiperImg(response);
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

        $.getJSON('/searchlist', params).done(function(response){
            if(response.code === 200){
                setTimeout(function(){
                    $(window).lazyLoadXT();
                }, 0);

                SearchList.showSearchList(response);
                SearchList.showSwiperImg(response);
            }else{
                alert(response.msg);
            }
        })
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
                                    '<img data-src="' + res.place_info[i].detail_image[0] + '" class="lazy-load card-img-fluid" alt="...">\n' +
                                '</div>\n' +
                            '</div>\n' +
                        '</div>\n' +
                        '<div class="card-body">\n' +
                            '<a class="h5 card-title fw-bolder" href="#">'+ res.place_info[i].place_name +'</a>\n' +
                            '<p class="card-text">95% 일치</p>\n' +
                            '<div class="col justify-content-md-center tags" id="tag' + (i+1) + '">\n' +
                            '</div>&nbsp;\n' +
                            '<p class="algo-text">Algo \n' +
                                '<span class="algo-star">★★★★★</span> \n' +
                            '</p> \n' +
                        '</div> \n' +
                    '</div> \n' +
                    '<br><br> \n' +
                '</div> \n'
            );

            for (var j=0; j<MAX_TAG; j++){
                if (res.place_info[i].tag[j] === undefined){
                    $('#tag'+ (i+1)).append(
                        '<button type="button" class="btn btn-secondary btn-sm" style="visibility:hidden;"></button>'
                    );
                }else{
                    $('#tag'+ (i+1)).append(
                    '<button type="button" class="btn btn-secondary btn-sm">\n' +
                        res.place_info[i].tag[j] +
                    '</button>\n'
                )}
            }
        }
        // 장소 클릭
        $('.col').each(function(idx){
            $(this).click(function(event){
                event.preventDefault();
                console.log(idx / 2);
                var id = res.place_info[Number(idx / 2)].content_id;
                var param = {
                    content_id: id
                }
                var url = '/detail?content_id=';
                location.href = url + encodeURI(encodeURIComponent(param.content_id));
            })
        })
    },
    showSwiperImg: function(res) {
        $(this).lazyLoadXT();
        for (var i = 0; i < res.place_info.length; i++) {
            for (var k = 1; k < res.place_info[i].detail_image.length; k++) {
                $('#swiper' + (i + 1)).append(
                    '<div class="swiper-slide">\n' +
                        '<img data-src="' + res.place_info[i].detail_image[k] + '"src="/static/imgs/test_img3.jpg"' + 'class="lazy-load card-img-fluid" alt="...">\n' +
                    '</div>\n'
                )
            }
        }
        var swiper = new Swiper(".mySwiper", {
            autoplay: {
                delay: 3500,
                disableOnInteraction: false,
            },
        });
    }
}

SearchList.sortList()
SearchList.getList()
