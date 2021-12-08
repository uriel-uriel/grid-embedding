const S = 700;
let mode = 1; // 0: node, 1: edge
let current_node;
let current_edge;
let nodes = [];
let edges = [];

function setup() {
  createCanvas(700, 700);
}

function draw() {
  background(23);
  stroke('#fafafa')
  strokeWeight(1)
  for (var i = S; i >= 0; i-=50) {
    line(0, i, S, i)
    line(i, 0, i, S)
  }
  if (mode) {
    where_da_line()
  } else {
    where_da_point()
  }
  
  drawAll()
}

function drawAll() {
  stroke(11, 230, 99)
  strokeWeight(3)
  edges.forEach(e => {
    line(e[0].x, e[0].y, e[1].x, e[1].y)
  })
  stroke(111, 230, 99)
  fill(111,250, 80)
  nodes.forEach(n => {
    circle(n.x, n.y, 10)
  })
}

function where_da_point() {
  const sX = mouseX
  const sY = mouseY
  const decx = sX % 50;
  const decy = sY % 50;
  
  const x = decx > 24 ? (sX - decx) + 50 : sX - decx
  const y = decy > 24 ? (sY - decy) + 50 : sY - decy
  stroke(111, 230, 99)
  fill(111,250, 80)
  current_node = {x:x, y:y}
  circle(x, y, 10);
}

function where_da_line() {
  const sX = mouseX
  const sY = mouseY
  const decx = sX % 50;
  const decy = sY % 50;
  
  stroke(11, 230, 99)
  strokeWeight(3)
  
  if (decx+decy <= 50 && decx > decy) {
    const x = Math.floor(sX/50) * 50;
    const y = Math.floor(sY/50) * 50;
    
    current_edge = [{x:x, y:y}, {x:x+50, y:y}]
    line(x, y, x+50, y);
  } else if (decx+decy <= 50 && decx <= decy) {
    const x = Math.floor(sX/50) * 50;
    const y = Math.floor(sY/50) * 50;
    
    current_edge = [{x:x, y:y}, {x:x, y:y+50}]
    line(x, y, x, y+50);
  } else if (decx+decy > 50 && decx > decy) {
    const x = Math.ceil(sX/50) * 50;
    const y = Math.floor(sY/50) * 50;
    
    current_edge = [{x:x, y:y}, {x:x, y:y+50}]
    line(x, y, x, y+50);
  } else {
    const x = Math.floor(sX/50) * 50;
    const y = Math.ceil(sY/50) *50;
    
    current_edge = [{x:x, y:y}, {x:x+50, y:y}]
    line(x, y, x+50, y);
  }
}

function mouseClicked() {
  if (mode === 0) {
    nodes.push(current_node);
  } else {
    edges.push(current_edge);
  }
}

function keyPressed() {
  if (keyCode === 77) {
    mode = (mode + 1) % 2
  } else if (keyCode === 80) {
    printGraph()
  }
}

function printGraph() {
  
}