window.onload = function(){
    var canvas = document.getElementById('background');
    var grass_num = 150;
    var sheep_num = 20;
    var wolf_num = 3;
    var time = 6000;
    var n_g = [];
    var n_s = [];
    var n_w = [];
    var labels = [];


    var ctx = canvas.getContext("2d");
    var maxWidth = canvas.width, maxHeight = canvas.height;
    ctx.fillRect(0, 0, maxWidth, maxHeight);
    
    function getRandomNum(minNum, maxNum) {
        return Math.round(
            Math.random() * (maxNum - minNum) + minNum);
    }

    // 草
    class Grass{
        constructor(){
            this.length = 15;
            this.color  = "#95ef5c";
            this.x = getRandomNum(this.length, maxWidth - this.length);
            this.y = getRandomNum(this.length, maxHeight - this.length);
        }
        draw(){
            ctx.beginPath();
            ctx.fillStyle = this.color;
            ctx.fillRect(this.x, this.y, this.length, this.length);
            ctx.fill();
            ctx.closePath();
        }
    }

    class Animal{
        constructor(){      
            this.r = 10;// 半径
            // 隨機坐标
            this.x = getRandomNum(this.r, maxWidth - this.r);
            this.y = getRandomNum(this.r, maxHeight - this.r);
            this.energy = 100;//生命值
        }
        draw() {
            ctx.beginPath();
            ctx.fillStyle = this.color;
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fill();
            ctx.closePath();
        }
    }

    // 羊
    class Sheep extends Animal{
        constructor(){
            super();
            this.color = '#ffffff';
            this.speed = 1;
        }
        move() {
            this.energy -= 0.1;
            let wolf_enemy = -1;
            let wolf_dis = [];
            let grass_dis = [];
            let SW_distance = [];
            let SG_distance = [];
            let run_direct = [];

            if(wolf_num > 0){
                for(let n = 0; n < wolf_num; n++){
                    wolf_dis[n] = (wolves[n].x-this.x)**2 + (wolves[n].y - this.y)**2
                    SW_distance.push(wolf_dis[n]);
                }
                SW_distance.sort(function(a, b) {return a - b;})
                wolf_enemy = wolf_dis.indexOf(SW_distance[0]);
                run_direct[0] = -1 * Math.sign(wolves[wolf_enemy].x-this.x);
                run_direct[1] = -1 * Math.sign(wolves[wolf_enemy].y-this.y);
            }
                if(wolf_enemy > -1 && wolf_dis[wolf_enemy] <= 5000){
                    this.x += run_direct[0] * this.speed;
                    this.y += run_direct[1] * this.speed;
                }
                else{
                    if(grass_num > 0){
                        // 抓最近的草
                        for(let n = 0; n < grass_num; n++){
                            grass_dis[n] = (grass[n].x-this.x)**2 + (grass[n].y - this.y)**2
                            SG_distance.push(grass_dis[n]);
                        }
                        SG_distance.sort(function(a, b) {return a - b;})
                        let grass_target = grass_dis.indexOf(SG_distance[0]); // 最近的草的index
    
                        let next_step = [(grass[grass_target].x-this.x), (grass[grass_target].y-this.y)];
                        if(next_step[0] > 0){
                            this.x += this.speed;
                        }
                        else if(next_step[0] < 0){
                            this.x -= this.speed;
                        }
                        if(next_step[1] > 0){
                            this.y += this.speed;
                        }
                        else if(next_step[1] < 0){
                            this.y -= this.speed;
                        }
                    }
                    else{
                        // 羊random走
                        this.x += getRandomNum(-1, 1) * this.speed;
                        this.y += getRandomNum(-1, 1) * this.speed;
                    }
                }
            
        }
        reproduce(){
            if (this.energy > 140){
                let newSheeps = new Sheep();
                sheeps.push(newSheeps);
                sheep_num += 1;
                this.energy -= 100;
            }
        }
    }    
    // 狼
    class Wolf extends Animal{
        constructor(){
            super();
            this.color = '#857263';
            this.speed = 1.5;
        }
        move(){
            this.energy -= 0.3;
            let WS_distance = [];
            let sheep_dis=[];
            if(sheep_num > 0){
                // 抓最近的羊
                for(let n = 0; n < sheep_num; n++){
                    sheep_dis[n] = (sheeps[n].x-this.x)**2 + (sheeps[n].y - this.y)**2
                    WS_distance.push(sheep_dis[n]);
                }
                WS_distance.sort(function(a, b) {return a - b;})
                let sheep_target = sheep_dis.indexOf(WS_distance[0]); // 最近的羊的index

                let next_step = [(sheeps[sheep_target].x-this.x), (sheeps[sheep_target].y-this.y)];
                if(next_step[0] > 0){
                    this.x += this.speed;
                }
                else if(next_step[0] < 0){
                    this.x -= this.speed;
                }
                if(next_step[1] > 0){
                    this.y += this.speed;
                }
                else if(next_step[1] < 0){
                    this.y -= this.speed;
                }
            }
            else{
                // 沒有羊就隨便走
                this.x += getRandomNum(-1, 1) * this.speed;
                this.y += getRandomNum(-1, 1) * this.speed;
            }
        }
        reproduce(){
            if (this.energy > 200){
                let newWolves = new Wolf();
                wolves.push(newWolves);
                wolf_num += 1;
                this.energy -= 100;
            }
        }
    }

    // 创建100个動物实例
    var grass = [];
    for (let i = 0; i < grass_num; i++) {
        let newGrass = new Grass();
        newGrass.draw();
        grass.push(newGrass);
    }
    var sheeps = [];
    for (let i = 0; i < sheep_num; i++) {
        let newSheeps = new Sheep();
        newSheeps.draw();
        sheeps.push(newSheeps);
    }
    var wolves = [];
    for (let i = 0; i < wolf_num; i++) {
        let newWolves = new Wolf();
        newWolves.draw();
        wolves.push(newWolves);
    }

    // 隨機生成草
    function grassGrow(n){
        if(getRandomNum(1, n) == 1){
            let newGrass = new Grass();
            grass.push(newGrass);
            grass_num += 1;
        }
    }

    // 羊吃草
    function eat_grass(g, s){
        grass_num -= 1;
        sheeps[s].energy += 30; //羊吃草增加10 energy
        grass.splice(g, 1);
        grassGrow(3);
    }
    // 狼吃羊
    function eat_sheep(s, w){
        sheep_num -= 1;
        wolves[w].energy += sheeps[s].energy/2; //狼吃羊增加羊1/3的energy
        sheeps.splice(s, 1);
    }

    function isDead(animals, n){
        if(animals == wolves){
            wolf_num -= 1;
            wolves.splice(n, 1);
        }
        else if(animals == sheeps){
            sheep_num -= 1;
            sheeps.splice(n, 1);
        }
    }

    var run = setInterval(() => {
        // 每次画之前都要清除画布
        ctx.clearRect(0, 0, maxWidth, maxHeight);
        ctx.fillStyle = '#afaa5b';
        ctx.fillRect(0, 0, maxWidth, maxHeight);
        
        grassGrow(4);
        for (let j = 0; j < grass_num; j++) {   
            grass[j].draw(ctx);
        }
        for (let j = 0; j < sheep_num; j++) {
            if(sheeps[j].energy > 0){
                sheeps[j].draw(ctx);
                sheeps[j].move();
                sheeps[j].reproduce();
            }
            else{
                isDead(sheeps, j);
            }
        }
        for (let j = 0; j < wolf_num; j++) {
            if(wolves[j].energy > 0){
                wolves[j].draw(ctx);
                wolves[j].move();
                wolves[j].reproduce();
            }
            else{
                isDead(wolves, j);
            }
        }        

        // 判斷羊有沒有吃到草
        for (let i = 0; i < grass_num; i++){
            for (let j = 0; j < sheep_num; j++){
                if (grass[i].x == sheeps[j].x && grass[i].y == sheeps[j].y){
                    eat_grass(i, j);
                }                
            }
        }
        // 判斷狼有沒有吃到羊
        for (let i = 0; i < sheep_num; i++){
            for (let j = 0; j < wolf_num; j++){
                if (sheeps[i].x == wolves[j].x && sheeps[i].y == wolves[j].y){
                    eat_sheep(i, j);
                }                
            }
        }
        console.log('grass:'+grass_num, 'sheep:'+sheep_num, 'wolf:'+wolf_num);

        if(time % 50 == 0){
            n_g.push(grass_num);
            n_s.push(sheep_num);
            n_w.push(wolf_num);
            labels.push(6000-time);
        }        
        if(time == 0 || (sheep_num == 0 && wolf_num == 0)){
            window.clearInterval(run);
            var chart = document.getElementById("chart").getContext("2d");
            drawLineCanvas(chart,lineChartData);
        }
        time -= 1;

    }, 1);

    function drawLineCanvas(chart,data) {
        window.myLine = new Chart(chart, {  //先建立一個 chart
            type: 'line', // 型態
            data: data,
            options: {
                    responsive: true,
                    legend: { //是否要顯示圖示
                        display: true,
                    },
                    tooltips: { //是否要顯示 tooltip
                        enabled: true
                    },
                    scales: {  //是否要顯示 x、y 軸
                        xAxes: [{
                            display: true
                        }],
                        yAxes: [{
                            id: "GS",
                            display: true,
                            position: 'left',
                        },{
                            id: "W",
                            display: true,
                            position: 'right',
                            ticks: {
                                max: 20,
                                min: 0
                            }
                        }]
                    },
                }
        });
    };

    var lineChartData = {
        labels: labels, //顯示區間名稱
        datasets: [{
            label: 'grass',
            borderColor: '#95ef5c',
            data: n_g, 
            yAxisID: "GS",
            fill: false,
        },{
            label: 'sheep',
            borderColor: '#e2ddd0',
            data: n_s, 
            yAxisID: "GS",
            fill: false,
        }, {
            label: 'wolf',
            borderColor: '#857263',
            data: n_w,
            yAxisID: "W",
            fill: false,
        },]
    };

        
}

