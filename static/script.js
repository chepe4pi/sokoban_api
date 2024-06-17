new Vue({
  el: '#app',
  data: {
    gameMap: [
      [0, 0, 0, 0, 0],
      [0, 1, 2, 3, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]
    ],
    playerPosition: { x: 1, y: 1 }
  },
  methods: {
    getCellClass(cell) {
      if (cell === 0) return 'cell';
      else if (cell === 1) return 'cell player';
      else if (cell === 2) return 'cell box';
      else if (cell === 3) return 'cell goal';
    },
    handleKey(event) {
      console.log('Key pressed: ', event.key);

      let newX = this.playerPosition.x;
      let newY = this.playerPosition.y;

      if (event.key === 'ArrowUp') newY--;
      else if (event.key === 'ArrowDown') newY++;
      else if (event.key === 'ArrowLeft') newX--;
      else if (event.key === 'ArrowRight') newX++;

      console.log(`Attempting to move to (${newX}, ${newY})`);

      let targetCell = this.gameMap[newY][newX];
      console.log(`Target cell value: ${targetCell}`);

      if (targetCell === 0 || targetCell === 3) {
        console.log('Moving player...');
        this.updatePlayerPosition(newX, newY);
      } else if (targetCell === 2) {
        let boxNewX = newX + (newX - this.playerPosition.x);
        let boxNewY = newY + (newY - this.playerPosition.y);

        console.log(`Attempting to move box to (${boxNewX}, ${boxNewY})`);

        if (this.gameMap[boxNewY][boxNewX] === 0 || this.gameMap[boxNewY][boxNewX] === 3) {
          console.log('Moving box...');
          this.gameMap[newY][newX] = 0;
          this.gameMap[boxNewY][boxNewX] = 2;
          this.updatePlayerPosition(newX, newY);
        }
      }
    },
    updatePlayerPosition(newX, newY) {
      console.log(`Updating player position to (${newX}, ${newY})`);
      this.gameMap[this.playerPosition.y][this.playerPosition.x] = 0;
      this.playerPosition.x = newX;
      this.playerPosition.y = newY;
      this.gameMap[newY][newX] = 1;
    }
  },
  mounted() {
    window.addEventListener('keydown', this.handleKey);
  },
  beforeDestroy() {
    window.removeEventListener('keydown', this.handleKey);
  }
});