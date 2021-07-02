const MAX_TAG = 3;

var SearchList = {

    lazy: function(){
        // $('img.lazy').Lazy({
        //     scrollDirection: 'vertical',
        //     effect: 'fadeIn',
        //     visibleOnly: true
        // })
    },

    getlist: function(){
        var param = document.location.href.split("?");
        var decode_param = decodeURI(decodeURIComponent(param[1].toString()));
        var req_param = decode_param.replaceAll('%3B', ';');
        var params = {
            keywords : req_param,
            res_num : '',
            place_info : '',
        }

        $.getJSON('/searchlist', params).done(function(response){
            if(response.code === 200){
                console.log(response);
                SearchList.showsearchlist(response)
            }else{
                alert(response.msg);
            }
        })
    },
    showsearchlist: function(res){
        $('.input-keyword').text(res.keywords);
        $('.input-size').text(res.res_num);

        for(var i=0; i<res.place_info.length; i++){
            $('#card-layout').append(
                '<div class="col">\n' +
                    '<div class="card border-0">\n' +
                        '<div class="swiper-container card mySwiper">\n' +
                            '<div class="swiper-wrapper" id="swiper'+ (i+1) + '">\n' +
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

            for(var k=0; k< res.place_info[i].detail_image.length; k++){

                $('#swiper'+ (i+1)).append(
                    '<div class="swiper-slide">\n' +
                        '<img src="' + res.place_info[i].detail_image[k] + '" class="card-img-fluid" onError="this.onerror=null;this.src=\'/static/imgs/test_img3.jpg\';" alt="...">\n' +
                    '</div>\n'
                    // '<div class="swiper-slide">\n' +
                    //     '<img class="lazy" src="' + res.place_info[i].detail_image[k] + '" loading="lazy" class="card-img-fluid" onError="this.onerror=null;this.src=\'/static/imgs/test_img3.jpg\';" alt="...">\n' +
                    // '</div>\n'
                )
            }

            var swiper = new Swiper(".mySwiper", {
                autoplay: {
                  delay: 2000,
                  disableOnInteraction: false
                }
            });
        }
    }
}
SearchList.lazy()
SearchList.getlist()
