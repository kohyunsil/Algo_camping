var DetailInfo = {
    getPlaceInfo: function(){
        var param = document.location.href.split("?content_id=");
        var decode_param = decodeURI(decodeURIComponent(param[1].toString()));
        var param = {
            content_id: decode_param
        }
        var access_token = DetailInfo.getCookie('access_token');

        // if(access_token !== undefined || typeof access_token !== 'undefined'){
        //     $.ajax({
        //         type : 'GET',
        //         url : '/detail/protected',
        //         headers : {
        //             Authorization : 'Bearer ' + access_token
        //         },
        //         data : param,
        //         dataType : 'json',
        //         success : function(response, status, xhr){
        //             DetailInfo.doAfterSuccess(response);
        //         },
        //         error : function(xhr, status, error){
        //             alert(error);
        //         }
        //     })
        // }else{
            $.getJSON('/detail/info', param).done(function(response){
                if (response.code === 200){
                    DetailInfo.doAfterSuccess(response);
                }else{
                    alert(response.msg);
                }
            })
        // }
    },
    showPlaceInfo: function(res){
        var star = '';

        if (res.avg_star === 0){
            $('.visitor-text').css({'visibility': 'hidden'});
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
                        '<img src="../imgs/test_img3.jpg" class="figure-img img-fluid rounded" onError="this.onerror=null;this.src=\'/static/imgs/algo_default.png\';" alt="...">\n' +
                '</div>\n'
            )
        }else{
            var img_array = res.place_info.detail_image.split(',');
            $('#swiper-place').empty();
            for(var i=0; i< img_array.length; i++){
                $('.swiper-wrapper').append(
                    '<div class="swiper-slide">\n' +
                            '<img src="' + img_array[i] + '" class="figure-img img-fluid rounded" onError="this.onerror=null;this.src=\'/static/imgs/algo_default.png\';" alt="...">\n' +
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
        var past = new Date(res.past_congestion[0].base_ymd);

        var basedate = base.getFullYear() + '-' + ('0'+(base.getMonth()+1)).slice(-2) + '-' + ('0' + base.getDate()).slice(-2);
        var pastdate = past.getFullYear() + '-' + ('0'+(past.getMonth()+1)).slice(-2) + '-' + ('0' + past.getDate()).slice(-2);
        var congestion = [];
        var daterange = [];

        for (var i=0; i<res.past_congestion.length; i++){
            congestion.push(res.past_congestion[i].congestion);
            var date = new Date(res.past_congestion[i].base_ymd);
            var ymd_date = date.getFullYear() + '-' + ('0'+(date.getMonth()+1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2);
            daterange.push(ymd_date);
        }
        // spider web (polar) chart
        Highcharts.chart('polar-container', {
            chart: {
              polar: true,
              type: 'line',
              backgroundColor: 'rgba(0,0,0,0)'
            },

            title: {
              text: '김알고님과 95% 일치합니다.'
            },

            credits:{
                enabled: false
            },

            subtitle: {
              text: '김알고님과 ' + res.place_info.place_name + '에 대한 분석결과입니다.'
            },

            pane: {
              size: '70%'
            },

            xAxis: {
              categories: ['COMFORT', 'CLEAN', 'HEALING', 'FUN', 'TOGETHER'],
              tickmarkPlacement: 'on',
              lineWidth: 0
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
              layout: 'vertical'
            },

            series: [{
                name: res.place_info.place_name,
                data: res.algo_score,
                pointPlacement: 'on'
            }],
            //{
            //   name: '사용자',
            //   data: [50000, 39000, 42000, 31000, 26000],
            //   pointPlacement: 'on'
            // }],

            responsive: {
              rules: [{
                condition: {
                  maxWidth: 500
                },
                chartOptions: {
                  legend: {
                    align: 'center',
                    verticalAlign: 'bottom',
                    layout: 'horizontal'
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
            backgroundColor: 'rgba(0,0,0,0)'
          },

          credits:{
            enabled: false
          },

          title: {
            text: res.place_info.place_name + '의 혼잡도'
          },

          subtitle: {
            text: pastdate + ' ~ '+ basedate + '기준'
          },
          plotOptions: {
            series: {
              label: {
                connectorAllowed: false
              },
              pointStart: 2000
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
              formatter: function() { return daterange[this.value]},
            }
          },
          legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
          },
          plotOptions: {
            series: [{
              label: {
                connectorAllowed: false
              },
              date: daterange
            }]
          },

          series: [{
            name: '지난' + res.past_congestion.length + '일 간 방문객 수',
            data: congestion
          }
          // , {
          //   name: '지난 1주일 간 방문율',
          //   data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
          // }
          ],

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
            backgroundColor: 'rgba(0,0,0,0)'
          },

          credits:{
            enabled: false
          },

          title: {
            text: res.place_info.place_name + '의 주요태그'
          },
          tooltip: {
            useHTML: true,
            pointFormat: '<b>{point.name}:</b> {point.value}m CO<sub>2</sub>'
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
                  color: 'black',
                  textOutline: 'none',
                  fontWeight: 'normal'
                }
              }
            }
          },
          series: [{
            name: '상위 5개 카테고리',
            data: [{
                name: '분위기 좋은',
                value: 767.1
              }, {
                name: '친절한',
                value: 600.7
              },{
                name: '별보기 좋은',
                value: 367.1
              },
              {
                name: '벌레가 없는',
                value: 100.7
            },
            {
                name: '근교',
                value: 200.1
            }]
          }]
        });
    },
    showLocalList: function(res){
        $('.mySwiper2').empty();
        $('.mySwiper2').append(
            '<div class="col">\n' +
                '<span>\n' +
                    '<h5 class="text-center"><span class="h5 user-name">김알고님</span>\n' +
                        '<span class="h5 fw-bold festival-addr" style="color: #49917D">' + res.place_info.addr.split(' ')[1] + '</span> 인근 축제/관광지는 어떠세요?\n' +
                    '</h5>\n' +
                '</span>\n' +
            '</div>\n' +
            '<div class="swiper-wrapper" id="swiper-local">\n' +
            '</div>'
        );
        for(var i=0; i<res.local_info.length; i++){
            if (res.local_info[i] === null){
                continue
            }else{
                if (res.local_info[i].line_intro === null){
                    res.local_info[i].line_intro = ' ';
                }
                $('#swiper-local').append(
                    '<div class="swiper-slide">\n' +
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
            autoplay: {
              delay: 2000,
              disableOnInteraction: false
            },
            lazy:{
                loadPrevNext: true,
                loadPrevNextAmount: 1,  // 미리 로드할 이미지 개수
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

        DetailInfo.showMap(response);
        DetailInfo.showPlaceInfo(response);
        DetailInfo.showHighCharts(response);
        DetailInfo.showLocalList(response);
    }
}
DetailInfo.getPlaceInfo();