var param = {
    content_id: '',
    id: '',
    access_token: '',
    status: 0
}
var like_list = [];
// header logo img 경로
$('.header-logo-img').attr('src', '/static/imgs/algo_logo2.png');

$('#empty-like').click(function(){
    param.status = 1; // like
    like_list.push(param.content_id);

    $.post('/user/like/update', param).done(function(response){
        if (response.code === 200){
            $('#empty-like').css({'display': 'none'});
            $('#nonempty-like').css('display', '');
        }else{
            alert('다시 시도해주세요.');
        }
    })
})


$('#nonempty-like').click(function(){
    param.status = 0 // dislike

    // content_id dislike (splice)
    var index = like_list.indexOf(param.content_id);
    if (index !== -1){
        like_list.splice(index, 1);
    }

    $.post('/user/like/update', param).done(function(response){
        if (response.code === 200){
            $('#nonempty-like').css({'display': 'none'});
            $('#empty-like').css('display', '');
        }else{
            alert('다시 시도해주세요.');
        }
    })
})

var DetailInfo = {
    IsSignin: function(){
        if (DetailInfo.getCookie('access_token') === undefined){
            $('#empty-like').css({'display': 'none'});
            $('#nonempty-like').css({'display': 'none'});
        }
    },
    getPlaceInfo: function(){
        var p_content_id = document.location.href.split("/")[4].toString();
        var p_id = document.location.href.split("/")[5].toString();
        var access_token = DetailInfo.getCookie('access_token');

        param.content_id = p_content_id;
        param.id = p_id;
        param.access_token = access_token;

        $.getJSON('/detail/info', param).done(function(response){
            if (response.code === 200){
                param.content_id = response.place_info.content_id;
                DetailInfo.doAfterSuccess(response);
            }else{
                alert(response.code);
            }
        })
    },
    showPlaceInfo: function(res){
        var star = '';
        if (res.avg_star === 0){
            $('.visitor-text').css({'visibility': 'hidden'});
            $('.visitoravg-info-btn').css({'display': 'none'});
        }
        $('.point').text(res.avg_star);
        $('#title').text(res.place_info.place_name);

        for (var i=0; i<parseInt(res.algo_star); i++){
            star += '★';
        }
        for (var i=0; i<(5 - parseInt(res.algo_star)); i++){
            star += '☆';
        }
        $('.algo-star').text(star + ' ');
        $('.algo-star').append(
            '<span class="detail-score">' + res.algo_star + '  ' + '</span>'
        );
        $('.addr').text(res.place_info.addr);
        $('.line-intro').text(res.place_info.line_intro);
        $('.tel').text(res.place_info.tel);
        $('.oper-date').text(res.place_info.oper_date + ' ' + res.place_info.oper_pd);
        $('.facility').text(res.place_info.industry);
        $('.homepage').text(res.place_info.homepage);
        $('.homepage').attr('href', res.place_info.homepage);
        $('.festival-addr').text(res.place_info.addr.split(' ')[1]);

        $('.swiper-banner').append(
            '<div class="swiper-container mySwiper">\n' +
            '<div class="swiper-wrapper" id="swiper-place">\n' +
            '</div>\n' +
            '</div>'
        );
        if (res.place_info.detail_image === null){
            $('#swiper-place').append(
                '<div class="swiper-slide">\n' +
                        '<img src="/static/imgs/test_img3.jpg" class="figure-img img-fluid rounded" onError="this.onerror=null;this.src=\'/static/imgs/algo_default.png\';" alt="...">\n' +
                '</div>\n'
            )
        }else{
            $('#swiper-place').empty();
            for(var i=0; i< res.place_info.detail_image.length; i++){
                $('.swiper-wrapper').append(
                    '<div class="swiper-slide">\n' +
                            '<img src="' + res.place_info.detail_image[i] + '" class="figure-img img-fluid rounded" onError="this.onerror=null;this.src=\'/static/imgs/algo_default.png\';" alt="...">\n' +
                    '</div>\n'
                )
            }
        }
        var swiper = new Swiper(".mySwiper", {
            autoplay: {
              delay: 3000,
              disableOnInteraction: false
            },
            lazy:{
                loadPrevNext: true,
                loadPrevNextAmount: 1,  // 미리 로드할 이미지 개수
            },
        });
    },
    showLikeIcon: function(res){
        if (res.like === 'None' || res.like === ''){
            $('#nonempty-like').css({'display': 'none'});
        }else{
            try{
                var like = res.like.split(',');
                for (var i=0; i<like.length; i++){
                    like_list.push(like[i]);
                }
                // content_id가 포함되어 있는지 확인
                if (like_list.includes(param.content_id.toString())){
                    $('#empty-like').css({'display': 'none'});
                }else{
                    $('#nonempty-like').css({'display': 'none'});
                }
            }catch (e) {

            }
        }
    },
    showMap: function(res){
        $('.kakao-map').append(
            '<div id="map" style="width:100%; height:100%;"></div>\n'
        )
        var container = document.getElementById('map');
        var options = {
            center: new window.kakao.maps.LatLng(res.place_info.lng, res.place_info.lat),
            level: 4
        };
        //지도 생성
        var map = new window.kakao.maps.Map(container, options);
        var marker = new kakao.maps.Marker({
            position: map.getCenter()
        });
        // 마커 표시
        marker.setMap(map);

        var iwContent = '<div class="h6 fw-bold" style="padding:4px;">' + res.place_info.place_name + '<br><p class="small fw-light text-muted">' + res.place_info.addr + '</p>',
        iwPosition = new kakao.maps.LatLng(res.place_info.lng, res.place_info.lat);

        // 인포윈도우 생성
        var infowindow = new kakao.maps.InfoWindow({
            position : iwPosition,
            content : iwContent
        });

        // 마커 위에 인포윈도우 표시
        infowindow.open(map, marker);
    },
    showHighCharts: function(res){
        var base = new Date();

        var basedate = base.getFullYear() + '-' + ('0'+(base.getMonth()+1)).slice(-2) + '-' + ('0' + base.getDate()).slice(-2);
        var avg_congestion = [];
        var sgg_congestion = [];
        var daterange = [];

        for (var i=0; i<res.congestion_obj.base_ymd.length; i++){
            sgg_congestion.push(res.congestion_obj.sgg_visitor[i]);
            avg_congestion.push(res.congestion_obj.avg_visitor[i]);
            daterange.push(res.congestion_obj.base_ymd[i].split(' ')[0]);
        }

        var tag = [];
        var colors = ['#49917d', '#e7cb01', '#c4c4c4'];
        // const SIZE = res.size;
        const SIZE = [1300, 900, 600, 300, 100];

        var algo_score_round = [];
        for (var i=0; i<res.algo_score.length; i++){
            algo_score_round.push(Math.round(res.algo_score[i] * 100) / 100);
        }

        for (var i=0; i<res.tag.length; i++){
            var bubbleinfo = {
                name: res.tag[i],
                value: SIZE[i],
                color: colors[0]
            }
            if (i === 0){
               bubbleinfo.color = colors[1];
            }
            if (i === res.tag.length - 1){
                bubbleinfo.color = colors[2];
            }
            tag.push(bubbleinfo);
        }

        if((DetailInfo.getCookie('access_token') === undefined)){
            $('#nonempty-like').css({'display': 'none'});
            $('#empty-like').css({'display': 'none'});

            var title = res.place_info.place_name + '에 대한 분석결과입니다.';
            var subtitle = '로그인을 통해 내 캠핑장 선호도를 파악하고 나와 캠핑장 매칭도를 확인해보세요.';
            var legend_name = '캠퍼';
        }
        else if((DetailInfo.getCookie('access_token') !== undefined) && (res.match_pct === false)){
            var title = res.place_info.place_name + '에 대한 분석결과입니다.';
            var subtitle = '설문 작성을 통해 내 캠핑장 선호도를 파악하고 나와 캠핑장 매칭도를 확인해보세요.';
            var legend_name = res.user_name + '님';
        }
        else if((DetailInfo.getCookie('access_token') !== undefined) && (res.match_pct !== false)){
            var title = res.user_name + '님과 ' + res.match_pct + '\% 일치합니다.';
            var subtitle = res.user_name + '님과 ' + res.place_info.place_name + '에 대한 분석결과입니다.';
            var legend_name = res.user_name + '님';
        }

        // spider web (polar) chart
        Highcharts.chart('polar-container', {
            chart: {
              polar: true,
              type: 'line',
              backgroundColor: 'rgba(0,0,0,0)'
            },
            title: {
              text: title
            },

            credits:{
                enabled: false
            },

            subtitle: {
              text: subtitle
            },

            pane: {
              size: '73%'
            },

            xAxis: {
              categories: ['COMFORT', 'CLEAN', 'HEALING', 'FUN', 'TOGETHER'],
              tickmarkPlacement: 'on',
              lineWidth: 0,
              labels: {
                  style: {
                      color: '#1f284a',
                      fontWeight: 'normal'
                  }
              }
            },

            yAxis: {
              gridLineInterpolation: 'polygon',
              lineWidth: 0,
              min: 0,
              max: 100
            },

            legend: {
              align: 'right',
              verticalAlign: 'middle',
              layout: 'horizontal'
            },

            series: [{
                name: res.place_info.place_name,
                data: algo_score_round,
                pointPlacement: 'on',
                color: '#4f9f88'
            },
            {
                name: legend_name,
                data: res.user_point,
                pointPlacement: 'on',
                color: '#1b4785'
            }],

            responsive: {
              rules: [{
                condition: {
                  maxWidth: 500
                },
                chartOptions: {
                  legend: {
                    align: 'center',
                    verticalAlign: 'bottom',
                    layout: 'vertical'
                  },
                  pane: {
                    size: '70%'
                  }
                }
              }]
            }
          });

        // line chart
        Highcharts.chart('line-container', {
          chart: {
            backgroundColor: 'rgba(0,0,0,0)',
          },

          credits:{
            enabled: false
          },

          title: {
            text: res.place_info.place_name + ' 방문객 추이'
          },

          subtitle: {
            text: daterange[0] + ' ~ '+ daterange[daterange.length -1] + ' 기준 방문객 수 추이'
          },
          plotOptions: {
            series: {
              label: {
                connectorAllowed: false
              },
              pointStart: 0,
            }
          },
          yAxis: {
            title: {
              text: '방문객 수'
            }
          },
          xAxis: {
            tickInterval: 1,
            labels: {
              enabled: true,
              formatter: function() { return daterange[this.value].split('2021-')[1]},
            }
          },
          legend: {
            // layout: 'vertical',
            // align: 'bottom',
            // verticalAlign: 'middle'
               layout: 'vertical',
               align: 'center',
               verticalAlign: 'bottom',
               itemMarginTop: 10,
               itemMarginBottom: 10
          },
          plotOptions: {
            series: [{
              label: {
                connectorAllowed: false
              },
              date: daterange,
            }]
          },
          series: [{
            name: res.place_info.place_name + ' 지역 방문객수',
            data: sgg_congestion,
            color: '#4f9f88'
          }
          , {
            name: '전국 평균 방문객수',
            data: avg_congestion,
            color: '#1b4785'
          }],
          responsive: {
            rules: [{
              condition: {
                maxWidth: 500
              },
              chartOptions: {
                legend: {
                  layout: 'horizontal',
                  align: 'center',
                  verticalAlign: 'bottom'
                }
              }
            }]
          }
        });

        // bubble chart
        Highcharts.chart('bubble-container', {
          chart: {
            type: 'packedbubble',
            backgroundColor: 'rgba(0,0,0,0)',
          },

          credits:{
            enabled: false
          },

          title: {
            text: res.place_info.place_name + '의 주요태그'
          },

          tooltip: {
            useHTML: true,
            pointFormat: '<b>{point.name}:</b> {point.value}'
          },

          plotOptions: {
            packedbubble: {
              minSize: '20%',
              maxSize: '100%',
              zMin: 0,
              zMax: 1000,
              layoutAlgorithm: {
                splitSeries: false,
                gravitationalConstant: 0.1
              },
              dataLabels: {
                enabled: true,
                format: '{point.name}',
                filter: {
                  property: 'y',
                  operator: '>',
                  value: 10 // visible filter
                },
                style: {
                  color: '#1f284a',
                  textOutline: 'none',
                  fontWeight: 'normal'
                }
              }
            }
          },
          series: [{
            name: res.place_info.place_name + '의 상위 5개 태그',
            data: tag,
            marker: {
                lineWidth: 1,
                lineColor: 'rgba(0,0,0,0)',
            }
          }]
        });
    },
    showLocalList: function(res){
        var user = '';
        $('.mySwiper2').empty();
        $('.mySwiper2').append(
            '<div class="col">\n' +
                '<span>\n' +
                    '<br><h5 class="text-center"><span class="h5 user-name"></span>' + '님 ' + '\n' +
                        '<span class="h5 fw-bold festival-addr" style="color: #49917D">' + res.place_info.addr.split(' ')[1] + '</span> 인근 축제/관광지는 어떠세요?\n' +
                    '</h5>\n' +
                '</span>\n' +
            '</div>\n' +
            '<div class="swiper-wrapper swiper-wrapper2" id="swiper-local">\n' +
            '</div>'
        );
        // 사용자 이름 노출
        if(DetailInfo.getCookie('access_token') === undefined){
            user = '캠퍼';
        }else{
            user = res.user_name;
        }
        $('.user-name').text(user);

        for(var i=0; i<res.local_info.length; i++){
            if (res.local_info[i] === null){
                continue
            }else{
                if (res.local_info[i].line_intro === null){
                    res.local_info[i].line_intro = ' ';
                }
                $('#swiper-local').append(
                    '<div class="swiper-slide swiper-slide2">\n' +
                        '<div class="h5 fw-bold local-title">' + res.local_info[i].place_name + '\n' +
                            '<span class="text-muted fw-normal small">'+ res.local_info[i].addr + '</span>\n' +
                        '</div>\n' +

                        '<div class="fw-light local-subtitle">' + res.local_info[i].line_intro + '</div><br>\n' +
                        '<img src="' + res.local_info[i].first_image + '" alt="..." onError="this.onerror=null;this.src=\'/static/imgs/algo_default.png\';">\n' +
                    '</div>'
                );
            }
        }
        var swiper2 = new Swiper('.mySwiper2', {
            spaceBetween: 10,
            autoplay: {
              delay: 2000,
              disableOnInteraction: false
            },
            lazy:{
                loadPrevNext: true,
                loadPrevNextAmount: 1,
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
    doAfterSuccess: function(response){
        $('.loading-bar').css({'visibility': 'hidden'});
        $('.container').css({'visibility': 'visible'});
        $('table').show();

        DetailInfo.showLikeIcon(response);
        DetailInfo.showMap(response);
        DetailInfo.showPlaceInfo(response);
        DetailInfo.showHighCharts(response);
        DetailInfo.showLocalList(response);
    },
    // linechart 리사이징
    redrawLineCharts: function(){
        var width = $('#line-chart-container').css('width');
        // $('#line-chart-container').css('width', '680px');
        // $('#line-chart-container').css('width', '33rem');
    }
}
DetailInfo.getPlaceInfo();
DetailInfo.redrawLineCharts();
DetailInfo.IsSignin();
