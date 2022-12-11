window.onload = function(){
    var canvas = document.getElementById('background');
    var sheep_num = 100;
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
        constructor(r, speed, x, y, energy, sheep, wolf){      
            // this.ctx = ctx;
            // this.maxWidth = maxWidth;
            // this.maxHeight = maxHeight;
            this.r = 10;// 半径
            // 随机x,y坐标
            this.x = getRandomNum(this.r, maxWidth - this.r);
            this.y = getRandomNum(this.r, maxHeight - this.r);
            this.speed = 20;// 平移速度,正负区间是为了移动方向多样
            this.energy = 100;
            this.sheep = 0;
            this.wolf = 0;
        }

        draw() {
            ctx.beginPath();
            ctx.fillStyle = this.color;
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fill();
            ctx.closePath();
        }
        move() {
            //!!!!!!!!!改成有傾向!!!!!!!!!!
            this.right = getRandomNum(-1, 1) * this.speed;
            this.left = getRandomNum(-1, 1) * this.speed;

            this.energy -= 1;
        }
    }

    // 羊
    class Sheep extends Animal{
        constructor(color){
            super();
            this.sheep = 1;
            this.color = '#ffffff';
        }
    }    
    // 狼
    class Wolf extends Animal{
        constructor(color){
            super();
            this.wolf = 1;
            this.color = '#857263';
        }
    }

    // 创建100个動物
    let square = [];
    for (let i = 0; i < maxWidth; i++) {
        for (let j = 0; j < maxHeight; j++) {
            let newSheeps = new Sheep(maxWidth, maxHeight, ctx);
            square.push(newSheeps);
            newSheeps.draw();
            let newWolves = new Wolf(maxWidth, maxHeight, ctx);
            square.push(newWolves);
            newWolves.draw();
        }
    }

    setInterval(() => {
        // 每次画之前都要清除画布
        ctx.clearRect(0, 0, maxWidth, maxHeight);
        ctx.fillStyle = '#95ef5c';
        ctx.fillRect(0, 0, maxWidth, maxHeight);
        for (let i = 0; i < maxWidth; i++) {
            for (let j = 0; j < maxHeight; j++) {
                if (square[i][j].sheep == 1 & square[i][j].wolf == 1){
                    eat_sheep(j, k);
                }  
                square[i][j].draw(ctx);
                square[i][j].move();    
            }
        }

        console.log('sheep:'+sheep_num, 'wolf:'+wolf_num);         
    }, 100);
}