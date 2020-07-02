
var chart;

window.onresize = function () {
    if(chart != null && chart != "" && chart != undefined){
         chart.resize(); 
    }
}
function dataRead(name, callback) {
    var dataList = new Array();
    //使用ajax加载csv文件的数据
    $.ajax({
        url: "data/" + name + ".csv",
        async: false, //同步请求
        success: function (result) {
            // 对csv文件的数据先以行分割
            var tempList = result.split("\n");
            // 我们在对每一行以逗号作分割
            for (var i = 0; i < 99; i++) {
                dataList[i] = new Array();
                tempAry = tempList[i + 1].split(",");
                for (j = 0; j < 7; j++) {
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
    rankType=nameList1[Math.floor(Math.random() % 13)];
    rankTime =nameList2[Math.floor(Math.random() % 3)];
    name=rankType+rankTime+"top100";
    console.log(name);
    num = Math.round(100 * Math.random());
    alert("即将为你打开" + rankType+rankTime+"榜第" + num + "个视频!");
    let dataList = dataRead(name,function (data){
        bv=data[num][6];
        window.open("http://www.bilibili.com/" +bv, "_blank");
    });
}

function myDraw(name) {
    x = [];
    y = [];
    let dataList = dataRead(name, function (data) {
        for (i = 0; i < 80; i++) {
            x.push(data[i][0]);
            y.push(data[i][4]);
        }
        if (chart != null && chart != "" && chart != undefined) {
            chart.dispose();//销毁
        }
        chart = echarts.init(document.getElementById('main'), 'purple-passion');
        var option = {
            title: {
                text: name
            },
            tooltip: {},
            xAxis: {
                data: x
            },
            yAxis: {},
            itemStyle: {
                normal: {
                    shadowBlur: 200,
                    // 阴影水平方向上的偏移
                    shadowOffsetX: 0,
                    // 阴影垂直方向上的偏移
                    shadowOffsetY: 0,
                    // 阴影颜色
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            },
            series: [{
                name: '视频得分',
                type: 'bar',
                data: y
            }]

        };
        chart.setOption(option);
    });
}