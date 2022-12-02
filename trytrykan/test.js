window.onload = function(){
    var canvas = document.getElementById('background');
    var sheep_num = 100;

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
            this.r = 20;
            // 随机x,y坐标
            this.x = getRandomNum(this.r, maxWidth - this.r);
            this.y = getRandomNum(this.r, maxHeight - this.r);
            // 平移速度,正负区间是为了移动方向多样
            this.speed = 20;
            // 颜色
            this.color = '#ffffff';
            this.energy = 100;
        }

        draw() {
            ctx.beginPath();
            ctx.fillStyle = this.color;
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fill();
            ctx.closePath();
        }
        move() {
            this.right = getRandomNum(-1, 1);
            this.left = getRandomNum(-1, 1);
            this.x += this.right * this.speed;
            this.y += this.left * this.speed;
            this.energy -= 1;
        }
    };
    // 创建100个Ball实例
    let balls = [];
    for (let i = 0; i < sheep_num; i++) {
        let newBall = new Animal(maxWidth, maxHeight, ctx);
        newBall.draw();
        balls.push(newBall);
    }

    setInterval(() => {
        // 每次画之前都要清除画布
        ctx.clearRect(0, 0, maxWidth, maxHeight);
        ctx.fillStyle = 'rgb(149, 239, 92)';
        ctx.fillRect(0, 0, maxWidth, maxHeight);
        for (let j = 0; j < 100; j++) {
            balls[j].draw(ctx);
            balls[j].move();
        }
    }, 100);
}

