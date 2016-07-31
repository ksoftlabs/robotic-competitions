#define WIDTH 30
#define HEIGHT 30
#define START_X 15
#define START_Y 15

byte grid[WIDTH][HEIGHT];

char direction = 'n';
int lastX = 0;
int lastY = 0;
int currentX = 0;
int currentY = 0;

void dryRun() {
  initializeArrays();

  while (!isOnJunction()) {
    readIRSensors();
    followLine();
  }

  //Mark junction (1,1)
  grid[START_X][START_Y] = 3;
  lastX = START_X;
  lastY = START_Y;

  turnLeft();
  changeDirection();

  while (true) {
    if (isOnBoundary() || isOnNode()) {
      turnBack();

      setCurrentPosition();
      setLastPosition();
      grid[currentX][currentY] = 0;
      reverseDirection();
    }
    else if (isOnBlockBase()) {
      turnBack();

      setCurrentPosition();
      setLastPosition();
      grid[currentX][currentY] = 4;
      reverseDirection();
    }
    else if(isOnJunction()){
      turnLeft();

      setCurrentPosition();
      setLastPosition();
      if (grid[currentX][currentY] == 0) {     //Non visited junction
        grid[currentX][currentY] = 3;
      }
      else if (grid[currentX][currentY] == 2) {   //Twice visited junction
        grid[currentX][currentY] = 1;
      }
      else if (grid[currentX][currentY] == 3) {     //Once visited junction
        grid[currentX][currentY] = 2;
      }
      else if (grid[currentX][currentY] == 1) {   //Starting point
        brake(10000);
      }
      changeDirection();
    }
  }
}

void initializeArrays() {
  for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
      grid[x][y] = 0;
    }
  }
}

void changeDirection() {
  if (direction == 'n') {
    direction = 'w';
  }
  else if (direction == 'e') {
    direction = 'n';
  }
  else if (direction == 's') {
    direction = 'e';
  }
  else if (direction == 'w') {
    direction = 's';
  }
}

void reverseDirection() {
  if (direction == 'n') {
    direction = 's';
  }
  else if (direction == 'e') {
    direction = 'w';
  }
  else if (direction == 's') {
    direction = 'n';
  }
  else if (direction == 'w') {
    direction = 'e';
  }
}

void setCurrentPosition() {
  if (direction == 'n') {
    currentY = lastY + 1;
  }
  else if (direction == 'e') {
    currentX = lastX + 1;
  }
  else if (direction == 's') {
    currentY = lastY - 1;
  }
  else if (direction == 'w') {
    currentX = lastX - 1;
  }
}

void setLastPosition() {
  lastX = currentX;
  lastY = currentY;
}
