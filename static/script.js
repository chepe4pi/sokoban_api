new Vue({
  el: '#app',
  data: {
    board: [
      [' ', ' ', ' ', ' ', ' '],
      [' ', '#', '#', '#', ' '],
      [' ', '#', '@', '$', ' '],
      [' ', '#', '.', '#', ' '],
      [' ', ' ', ' ', ' ', ' '],
    ],
    playerPosition: { x: 2, y: 2 }
  },
  methods: {
    movePlayer(dx, dy) {
      const newX = this.playerPosition.x + dx;
      const newY = this.playerPosition.y + dy;

      if (this.board[newY][newX] === '#') return;

      if (this.board[newY][newX] === '$') {
        const boxNewX = newX + dx;
        const boxNewY = newY + dy;

        if (this.board[boxNewY][boxNewX] === ' ' || this.board[boxNewY][boxNewX] === '.') {
          this.$set(this.board[newY], newX, ' ');
          this.$set(this.board[boxNewY], boxNewX, '$');
        } else {
          return;
        }
      }

      this.$set(this.board[this.playerPosition.y], this.playerPosition.x, ' ');
      this.$set(this.board[newY], newX, '@');
      this.playerPosition.x = newX;
      this.playerPosition.y = newY;
    },
    handleKeydown(event) {
      switch (event.key) {
        case 'ArrowUp':
          this.movePlayer(0, -1);
          break;
        case 'ArrowDown':
          this.movePlayer(0, 1);
          break;
        case 'ArrowLeft':
          this.movePlayer(-1, 0);
          break;
        case 'ArrowRight':
          this.movePlayer(1, 0);
          break;
      }
    }
  },
  mounted() {
    window.addEventListener('keydown', this.handleKeydown);
  },
  beforeDestroy() {
    window.removeEventListener('keydown', this.handleKeydown);
  },
  template: `
    <div id="game-board">
      <div v-for="(row, rowIndex) in board" :key="rowIndex">
        <div v-for="(cell, cellIndex) in row" :key="cellIndex" :class="getClass(cell)">
          {{ cell }}
        </div>
      </div>
    </div>
  `,
  computed: {
    getClass() {
      return (cell) => {
        switch(cell) {
          case '#': return 'cell wall';
          case '@': return 'cell player';
          case '$': return 'cell box';
          case '.': return 'cell target';
          default: return 'cell';
        }
      }
    }
  }
});