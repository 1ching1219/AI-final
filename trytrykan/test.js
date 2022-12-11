window.onload = function(){
    var canvas = document.getElementById('background');
    var sheep_num = 200;
    var wolf_num = 50;

    var ctx = canvas.getContext("2d");
    var maxWidth = canvas.width, maxHeight = canvas.height;
    ctx.fillRect(0, 0, maxWidth, maxHeight);
    
    function getRandomNum(minNum, maxNum) {
        switch (arguments.length) {
            case 1:
                return Math.round(Math.random() * minNum + minNum);
                break;
            case 2:
                return Math.round(
                    Math.random() * (maxNum - minNum) + minNum);
                break;
            case 0:
                return 0;
                break;
        }
    }

    class Animal{
        constructor(r, speed, x, y, energy){      
            // this.ctx = ctx;
            // this.maxWidth = maxWidth;
            // this.maxHeight = maxHeight;
            // 随机半径
            this.r = 10;
            随机x,y坐标
            this.x = getRandomNum(this.r, maxWidth - this.r);
            this.y = getRandomNum(this.r, maxHeight - this.r);
            // this.x = getRandomNum(1, maxWidth/(this.r*2)) * this.r*2 + this.r;
            // this.y = getRandomNum(1, maxHeight/(this.r*2)) * this.r*2 +this.r;
            // 平移速度,正负区间是为了移动方向多样
            this.speed = this.r*2;
            // 颜色
            this.energy = 100;
        }

        draw() {
            ctx.beginPath();
            ctx.fillStyle = this.color;
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fill();
            ctx.closePath();
        }
        // move() {
        //     this.x += getRandomNum(-1, 1) * this.speed;
        //     this.y += getRandomNum(-1, 1) * this.speed;
        //     this.energy -= 1;
        // }
    }

    // 羊
    class Sheep extends Animal{
        constructor(color){
            super();
            this.color = '#ffffff';
        }
        move() {
            this.x += getRandomNum(-1, 1) * this.speed;
            this.y += getRandomNum(-1, 1) * this.speed;
            this.energy -= 1;
        }
    }    
    // 狼
    class Wolf extends Animal{
        constructor(color){
            super();
            this.color = '#857263';
        }
        move(){
            let k = 1;
            for(let i = k*(-1); i <= k; i++){
                for(let j = k*(-1); j <= k; j++){
                    for(let n = 0; n < sheep_num; n++){
                        super();
                        if(this.x + i == sheeps[n].x & this.y + j == sheeps[n].y){
                            this.x += i * this.speed;
                            this.y += j * this.speed;
                        }
                        else{
                            continue;
                        }
                    }
                }
            }     
        }
    }

    // 创建100个動物实例
    let sheeps = [];
    for (let i = 0; i < sheep_num; i++) {
        let newSheeps = new Sheep(maxWidth, maxHeight, ctx);
        newSheeps.draw();
        sheeps.push(newSheeps);
    }
    let wolves = [];
    for (let i = 0; i < wolf_num; i++) {
        let newWolves = new Wolf(maxWidth, maxHeight, ctx);
        newWolves.draw();
        wolves.push(newWolves);
    }

    // 狼吃羊
    function eat_sheep(s, w){
        sheep_num -= 1;
        // sheeps[s].energy = 0;
        wolves[w].energy += 50; //狼吃羊增加50 energy
        sheeps.splice(s, 1);
    }

    // function isDead(){
        // if(energy )
    // }

    setInterval(() => {
        // 每次画之前都要清除画布
        ctx.clearRect(0, 0, maxWidth, maxHeight);
        ctx.fillStyle = '#95ef5c';
        ctx.fillRect(0, 0, maxWidth, maxHeight);
        for (let j = 0; j < sheep_num; j++) {
            sheeps[j].draw(ctx);
            sheeps[j].move();
        }
        for (let j = 0; j < wolf_num; j++) {
            wolves[j].draw(ctx);
            wolves[j].move();
        }

        console.log('sheep:'+sheep_num, 'wolf:'+wolf_num);

        for (let i = 0; i < sheep_num; i++){
            for (let j = 0; j < wolf_num; j++){
                if (sheeps[i].x == wolves[j].x & sheeps[i].y == wolves[j].y){
                    eat_sheep(i, j);
                }                
            }
        }
            

    }, 100);
}

