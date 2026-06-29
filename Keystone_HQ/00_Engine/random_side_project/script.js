const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

const cols = 100;
const rows = 100;
const w = canvas.width / cols;

// 0: Empty, 1: Sand, 2: Water, 3: Wood, 4: Wet Concrete, 5: Solid Concrete
let grid = make2DArray(cols, rows);
let nextGrid = make2DArray(cols, rows);

// To handle concrete hardening
let ageGrid = make2DArray(cols, rows);

let currentTool = 1;
let isDrawing = false;

// Tool selection
document.querySelectorAll('.tool').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.tool').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentTool = parseInt(e.target.getAttribute('data-tool'));
    });
});

document.getElementById('clear').addEventListener('click', () => {
    grid = make2DArray(cols, rows);
    ageGrid = make2DArray(cols, rows);
});

// Mouse interaction
canvas.addEventListener('mousedown', () => isDrawing = true);
canvas.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mouseleave', () => isDrawing = false);
canvas.addEventListener('mousemove', (e) => {
    if (isDrawing) {
        let rect = canvas.getBoundingClientRect();
        let mouseX = e.clientX - rect.left;
        let mouseY = e.clientY - rect.top;
        let i = Math.floor(mouseX / w);
        let j = Math.floor(mouseY / w);
        
        let brushSize = currentTool === 3 || currentTool === 0 ? 3 : 2; // Thicker brush for wood and eraser
        for(let x = -brushSize; x <= brushSize; x++) {
            for(let y = -brushSize; y <= brushSize; y++) {
                // Circular brush approximation
                if (x*x + y*y <= brushSize*brushSize) {
                    if (Math.random() > 0.2 || currentTool === 3 || currentTool === 0) {
                        let col = i + x;
                        let row = j + y;
                        if (col >= 0 && col < cols && row >= 0 && row < rows) {
                            grid[col][row] = currentTool;
                            ageGrid[col][row] = 0;
                        }
                    }
                }
            }
        }
    }
});

function make2DArray(cols, rows) {
    let arr = new Array(cols);
    for (let i = 0; i < arr.length; i++) {
        arr[i] = new Array(rows).fill(0);
    }
    return arr;
}

const colors = {
    0: '#000000',
    1: '#ffd700', // Sand
    2: '#4169e1', // Water
    3: '#8b4513', // Wood
    4: '#7a7a7a', // Wet Concrete
    5: '#b0b0b0'  // Solid Concrete
};

function draw() {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            let state = grid[i][j];
            if (state > 0) {
                ctx.fillStyle = colors[state];
                ctx.fillRect(i * w, j * w, w, w);
            }
        }
    }
}

function update() {
    // Reset nextGrid
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            nextGrid[i][j] = 0;
        }
    }

    for (let i = 0; i < cols; i++) {
        for (let j = rows - 1; j >= 0; j--) {
            let state = grid[i][j];
            if (state === 0) continue;
            
            if (state === 3 || state === 5) {
                // Wood and Solid Concrete don't move
                nextGrid[i][j] = state;
                continue;
            }

            let below = j + 1 < rows ? grid[i][j + 1] : -1;
            let belowNext = j + 1 < rows ? nextGrid[i][j + 1] : -1;

            if (state === 1) { // Sand
                if (below === 0 && belowNext === 0) {
                    nextGrid[i][j + 1] = state;
                } else {
                    let dir = Math.random() < 0.5 ? 1 : -1;
                    let bLeft = (i - dir >= 0 && j + 1 < rows) ? grid[i - dir][j + 1] : -1;
                    let bRight = (i + dir < cols && j + 1 < rows) ? grid[i + dir][j + 1] : -1;
                    
                    let bnLeft = (i - dir >= 0 && j + 1 < rows) ? nextGrid[i - dir][j + 1] : -1;
                    let bnRight = (i + dir < cols && j + 1 < rows) ? nextGrid[i + dir][j + 1] : -1;

                    // Sand can fall through water
                    if ((bLeft === 0 || bLeft === 2) && (bnLeft === 0 || bnLeft === 2)) {
                        nextGrid[i - dir][j + 1] = state;
                        if(bLeft === 2) nextGrid[i][j] = 2; // displace water
                    } else if ((bRight === 0 || bRight === 2) && (bnRight === 0 || bnRight === 2)) {
                        nextGrid[i + dir][j + 1] = state;
                        if(bRight === 2) nextGrid[i][j] = 2; // displace water
                    } else {
                        nextGrid[i][j] = state;
                    }
                }
            } else if (state === 2 || state === 4) { // Water and Wet Concrete
                // Concrete hardens over time
                if (state === 4) {
                    ageGrid[i][j]++;
                    // Hardens after some time probabilistically
                    if (ageGrid[i][j] > 200 + Math.random() * 100) {
                        nextGrid[i][j] = 5; // Turns to solid concrete
                        continue;
                    }
                }

                let isConcrete = (state === 4);
                let flowRate = isConcrete ? 0.3 : 0.8; // Concrete flows slower and less often

                if (below === 0 && belowNext === 0) {
                    nextGrid[i][j + 1] = state;
                    if(isConcrete) ageGrid[i][j+1] = ageGrid[i][j];
                } else {
                    let dir = Math.random() < 0.5 ? 1 : -1;
                    let bLeft = (i - dir >= 0 && j + 1 < rows) ? grid[i - dir][j + 1] : -1;
                    let bRight = (i + dir < cols && j + 1 < rows) ? grid[i + dir][j + 1] : -1;
                    
                    let bnLeft = (i - dir >= 0 && j + 1 < rows) ? nextGrid[i - dir][j + 1] : -1;
                    let bnRight = (i + dir < cols && j + 1 < rows) ? nextGrid[i + dir][j + 1] : -1;
                    
                    if (bLeft === 0 && bnLeft === 0 && Math.random() < flowRate) {
                        nextGrid[i - dir][j + 1] = state;
                        if(isConcrete) ageGrid[i-dir][j+1] = ageGrid[i][j];
                    } else if (bRight === 0 && bnRight === 0 && Math.random() < flowRate) {
                        nextGrid[i + dir][j + 1] = state;
                        if(isConcrete) ageGrid[i+dir][j+1] = ageGrid[i][j];
                    } else {
                        // Flow horizontally
                        let left = (i - dir >= 0) ? grid[i - dir][j] : -1;
                        let right = (i + dir < cols) ? grid[i + dir][j] : -1;
                        let nLeft = (i - dir >= 0) ? nextGrid[i - dir][j] : -1;
                        let nRight = (i + dir < cols) ? nextGrid[i + dir][j] : -1;

                        if (left === 0 && nLeft === 0 && Math.random() < flowRate) {
                            nextGrid[i - dir][j] = state;
                            if(isConcrete) ageGrid[i-dir][j] = ageGrid[i][j];
                        } else if (right === 0 && nRight === 0 && Math.random() < flowRate) {
                            nextGrid[i + dir][j] = state;
                            if(isConcrete) ageGrid[i+dir][j] = ageGrid[i][j];
                        } else {
                            nextGrid[i][j] = state;
                            if(isConcrete) ageGrid[i][j] = ageGrid[i][j];
                        }
                    }
                }
            }
        }
    }
    
    // Swap grids
    let temp = grid;
    grid = nextGrid;
    nextGrid = temp;
}

// Ensure simulation runs smoothly
let lastTime = 0;
function loop(time) {
    if (time - lastTime > 1000/60) { // Limit to 60 FPS
        update();
        draw();
        lastTime = time;
    }
    requestAnimationFrame(loop);
}

loop(0);
