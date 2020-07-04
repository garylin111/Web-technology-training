var chart1, chart2, chart3;

window.onresize = function () {
    chart1.resize();
    chart2.resize();
    chart3.resize();
}

function ourPage() {
    alert("即将为你打开三个人才的自我介绍网页");
    window.open("ykh.html", 'one');
    window.open("cc.html", 'two');
    window.open("lzj.html", 'three');
}

function dataRead(name, callback) {
    var dataList = new Array();
    //使用ajax加载csv文件的数据
    console.log(name);
    $.ajax({
        url: "data/" + name + ".csv",
        async: false, //同步请求
        success: function (result) {
            // 对csv文件的数据先以行分割
            var tempList = result.split("\n");
            // 我们在对每一行以逗号作分割
            for (var i = 0; i < tempList.length - 1; i++) {
                dataList[i] = new Array();
                tempAry = tempList[i + 1].split(",");
                for (j = 0; j < tempAry.length; j++) {
                    dataList[i][j] = tempAry[j];
                }
            }
        }
    });
    callback(dataList);
}

function randVideo() {
    var nameList1 = ["全站", "动画", "国创相关", "音乐", "舞蹈", "游戏", "知识", "数码", "生活", "鬼畜", "时尚", "娱乐", "影视"]
    var nameList2 = ["月排行", "周排行", "日排行"];
    rankType = nameList1[Math.floor(Math.random() % 13)];
    rankTime = nameList2[Math.floor(Math.random() % 3)];
    name = rankType + rankTime + "top100";
    num = Math.round(100 * Math.random());

    let dataList = dataRead(name, function (data) {
        bv = data[num][0];
        videoName = data[num][5];
        upName = data[num][1];
        alert("即将为你打开" + rankType + rankTime + "榜第" + num + "个视频!\n" + upName + "的" + "====" + videoName + "====");
        window.open("http://www.bilibili.com/" + bv, "_blank");
    });
}

function myDraw(name) {
    rankList = [];
    pointsLits = [];
    coinsList = [];
    playTimesList = [];
    danmakuList = [];
    let dataList = dataRead(name, function (data) {
        for (i = 0; i < 100; i++) {
            rankList.push(String(i + 1));
            pointsLits.push(data[i][4]);
            playTimesList.push(data[i][3]);
            coinsList.push(data[i][2]);
            danmakuList.push(data[i][6]);
        }
        if (chart1 != null && chart1 != "" && chart1 != undefined) {
            chart1.dispose(); //销毁
        }
        if (chart2 != null && chart2 != "" && chart2 != undefined) {
            chart2.dispose(); //销毁
        }
        chart1 = echarts.init(document.getElementById('main1'), 'purple-passion');
        chart2 = echarts.init(document.getElementById('main2'), 'purple-passion');

        var option1 = {
            legend: {
                top: '10%'
            },
            title: {
                subtext: "    " + name,
                x: 'left'
            },
            subtextStyle: {
                fontSize: 20
            },
            tooltip: {
                trigger: 'axis', //按轴选定
                showContent: true
            },
            dataset: {
                source: [
                    ['排名'].concat(rankList),
                    ['得分'].concat(pointsLits),
                    ['播放量'].concat(playTimesList),
                ]
            },
            xAxis: [{
                name: '排名',
                type: 'category',
                data: rankList
            }, {
                name: '排名',
                type: 'category',
                data: rankList,
                gridIndex: 1
            }],
            yAxis: [{
                gridIndex: 0
            }, {
                gridIndex: 1
            }],
            grid: [

                {
                    bottom: '60%',
                    left: '20%',
                    right: 50,
                }, {
                    top: '60%',
                    left: '20%',
                    right: 50,
                }
            ],
            series: [{
                    name: '视频得分',
                    type: 'bar',
                    seriesLayoutBy: 'row',
                    encode: {
                        x: '排名',
                        y: '得分'
                    }
                },
                {
                    name: '视频播放量',
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    encode: {
                        x: '排名',
                        y: '播放量'
                    },
                    xAxisIndex: 1,
                    yAxisIndex: 1
                },
            ]
        };
        var option2 = {
            legend: {
                top: '15%'
            },
            title: {
                subtext: "    " + name + '  硬币与弹幕',
                x: 'left'
            },
            subtextStyle: {
                fontSize: 20
            },
            tooltip: {
                trigger: 'axis', //按轴选定
                showContent: true
            },
            dataset: {
                source: [
                    ['排名'].concat(rankList),
                    ['硬币数'].concat(coinsList),
                    ['弹幕数'].concat(danmakuList)
                ]
            },
            xAxis: {
                name: '排名',
                type: 'category',
                data: rankList
            },
            yAxis: {
                min: 0
            },
            grid: {
                left: '20%',
                right: 50,
            },
            series: [{
                    name: '硬币',
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    encode: {
                        x: '排名',
                        y: '硬币数'
                    }
                },
                {
                    name: '弹幕',
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    encode: {
                        x: '排名',
                        y: '弹幕数'
                    }
                },
                {
                    type: 'pie',
                    id: 'pie',
                    radius: '20',
                    center: ['80%', '30%'],
                    label: {
                        formatter: '{b}: {@1} ({d}%)'
                    },
                    encode: {
                        itemName: '排名',
                        value: '1',
                        tooltip: '1'
                    }
                }
            ]
        };
        chart2.on('updateAxisPointer', function (event) { //监听鼠标，改变饼图值
            var xAxisInfo = event.axesInfo[0];
            if (xAxisInfo) {
                var dimension = xAxisInfo.value + 1;
                chart2.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                        },
                        encode: {
                            value: dimension,
                            tooltip: dimension
                        }
                    }
                });
            }
        });
        chart1.setOption(option1);
        chart2.setOption(option2);
    });
    sumDraw(name);
}

function sumDraw(name) {
    docName = 'sum/' + name.substr(name.length - 9, 3) + '总和';
    //console.log(name);
    playTimesList = [];
    coinsList = [];
    nameList = []; //分区名
    if (chart3 != null && chart3 != "" && chart3 != undefined) {
        chart3.dispose(); //销毁
    }
    chart3 = echarts.init(document.getElementById('main3'), 'purple-passion');
    let dataList = dataRead(docName, function (data) {
        for (i = 1; i < 13; i++) {
            nameList.push(data[i][0]);
            playTimesList.push(data[i][1]);
            coinsList.push(data[i][2]);
        }
        console.log(nameList);
        console.log(playTimesList);
        console.log(coinsList);
        var option3 = {
            title: [
                {subtext: "    "+name.substr(name.length - 9, 3) +"分区比例",
                x: 'left'},
                {
                    subtext: '弹幕数',
                    left: '25%',
                    top: '65%',
                    textAlign: 'center'
                },{
                    subtext: '硬币数',
                    left: '75%',
                    top: '65%',
                    textAlign: 'center'
                },
            ],
            grid: 
                {
                bottom: '60%',
                left: '20%',
                right: 50,
            }, 
            tooltip: {
                trigger: 'item',
                formatter: '<br/>{c} ({d}%)'
            },
            legend: {top: '15%'},
            subtextStyle: {
                fontSize: 20
            },
            dataset: {
                source: [
                    ['分区'].concat(nameList),
                    ['硬币'].concat(coinsList),
                    ['播放量'].concat(playTimesList),
                ]
            },
            series: [{
                name: '硬币数',
                type: 'pie',
                radius: '50',
                center: ['25%', '50%'],
                seriesLayoutBy: 'row',
                roseType: 'radius',
                encode: {
                    itemName: '分区',
                    value: '硬币',
                    tooltip: '硬币'
                }
            }, {
                name: '播放量',
                type: 'pie',
                radius: '50',
                center: ['75%', '50%'],
                seriesLayoutBy: 'row',
                encode: {
                    itemName: '分区',
                    value: '播放量',
                    tooltip: '播放量'
                }
            }]
        };
        chart3.setOption(option3);
    });
}