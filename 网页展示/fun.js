var vlist1 = [];
var vlist2 = [];
var myChart;
window.onload = function () {
    myChart = echarts.init(document.getElementById('main'));
}
window.onresize = function(){
    console.log("resizing");
    myChart.resize();
} 
function dataRead() {
    vlist1=[];
    vlist2=[];
    //使用ajax加载csv文件的数据
    $.ajax({
        url: "./全站周排行top100.csv",
        success: function (result) {
            // 对csv文件的数据先以行分割
            userList = result.split("\n");
            // 我们在对每一行以逗号作分割
            for (i = 1; i < userList.length; i++) {
                userary = userList[i].split(",");
                vlist1.push(userary[0]);
                vlist2.push(Number(userary[4]));
            }
        }
    });
}
function draw() {
    // 基于准备好的dom，初始化echarts实例
    // 指定图表的配置项和数据
    myChart.dispose();
    myChart = echarts.init(document.getElementById('main'));
    var option = {
        title: {
            text: 'ECharts 实例'
        },
        tooltip: {},
        legend: {
            data: ['视频得分']
        },
        xAxis: {
            data: vlist1
        },
        yAxis: {},
        series: [{
            name: '视频得分',
            type: 'bar',
            data: vlist2
        }]
    };
    myChart.setOption(option)
}
