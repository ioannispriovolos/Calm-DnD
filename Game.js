import React from 'react';
import './Game.css';
import fire from './fire';
import Checkbox from './Checkbox';

const CELL_SIZE = 80;
const WIDTH = 801;
const HEIGHT = 641;

const items = [
  'Project',
  'Set trap(s)',
  'Hobgoblin',
  'Orc',
  'Troll',
  'Gnoll',
  'Ogre',
  'Fire from:',
  'Fire to:',
]

var z = '';

class Cell extends React.Component {

    render() {
        const { x, y } = this.props;
        return (
            <div className="Cell" style={{
                left: `${CELL_SIZE * x + 1}px`,
                top: `${CELL_SIZE * y + 1}px`,
                width: `${CELL_SIZE - 1}px`,
                height: `${CELL_SIZE - 1}px`,
            }} />
        );
    }
}

class Game extends React.Component {
  constructor() {
        super();
        this.rows = HEIGHT / CELL_SIZE;
        this.cols = WIDTH / CELL_SIZE;

        this.board = this.makeEmptyBoard();
  }

  state = {
        cells: [],
  }

  makeEmptyBoard() {
        let board = [];
        for (let y = 0; y < this.rows; y++) {
            board[y] = [];
            for (let x = 0; x < this.cols; x++) {
                board[y][x] = false;
            }
        }
        return board;
  }

  getElementOffset() {
        const rect = this.boardRef.getBoundingClientRect();
        const doc = document.documentElement;

        return {
	    x: (rect.left + window.pageXOffset) - doc.clientLeft,
            y: (rect.top + window.pageYOffset) - doc.clientTop,
        };
  }

  makeCells() {
        let cells = [];
        for (let y = 0; y < this.rows; y++) {
            for (let x = 0; x < this.cols; x++) {
                if (this.board[y][x]) {
                    cells.push({ x, y });
                }
            }
        }
        return cells;
  }

  componentWillMount = () => {
    this.selectedCheckboxes = new Set();
  }

  toggleCheckbox = label => {
    if (this.selectedCheckboxes.has(label)) {
      this.selectedCheckboxes.delete(label);
    } else {
      this.selectedCheckboxes.add(label);
      z = label;
    }
  }

  handleFormSubmit = formSubmitEvent => {
    formSubmitEvent.preventDefault();

    for (const checkbox of this.selectedCheckboxes) {
      console.log(checkbox, 'is selected.');
    }
  }

  createCheckbox = label => (
    <Checkbox
            label={label}
            handleCheckboxChange={this.toggleCheckbox}
            key={label}
        />
  )

  createCheckboxes = () => (
  items.map(this.createCheckbox)
  )

  handleClick = (event) => {

        const elemOffset = this.getElementOffset();
        const offsetX = event.pageX - elemOffset.x;
        const offsetY = event.pageY - elemOffset.y;
        
        const x = Math.floor(offsetX / CELL_SIZE);
        const y = Math.floor(offsetY / CELL_SIZE);

        if (x >= 0 && x <= this.cols && y >= 0 && y <= this.rows) {
            this.board[y][x] = !this.board[y][x];
        }

        this.setState({ cells: this.makeCells() });

	alert(z);

	if (z === 'Project') {
		var ref = fire.database().ref('click');
	
		ref.push({x, y});
	}

	else if (z === 'Set trap(s)') {
		var ref = fire.database().ref('traps');
	
		ref.push({x, y});
	}

	else if (z === 'Hobgoblin') {
		var ref = fire.database().ref('monsters');
	
		ref.push({x, y, z});
	}

	else if (z === 'Orc') {
		var ref = fire.database().ref('monsters');
	
		ref.push({x, y, z});
	}

	else if (z === 'Troll') {
		var ref = fire.database().ref('monsters');
	
		ref.push({x, y, z});
	}

	else if (z === 'Gnoll') {
		var ref = fire.database().ref('monsters');
	
		ref.push({x, y, z});
	}

	else if (z === 'Ogre') {
		var ref = fire.database().ref('monsters');
	
		ref.push({x, y, z});
	}	
	
	else if (z === 'Fire from:') {
		var ref = fire.database().ref('attack/from');
	
		ref.push({x, y});
	}
	else if (z === 'Fire to:') {
		var ref = fire.database().ref('attack/to');
	
		ref.push({x, y});
	}		
  }

  render() {
    const { cells } = this.state;
    return (
      <div>
        <div className="Board"
          style={{ width: WIDTH, height: HEIGHT,
            backgroundSize: `${CELL_SIZE}px ${CELL_SIZE}px`}}
          onClick={this.handleClick}
          ref={(n) => { this.boardRef = n; }}>
          {cells.map(cell => (
            <Cell x={cell.x} y={cell.y}
                key={`${cell.x},${cell.y}`}/>
          ))}
        </div>

        <div className="row">
          <div className="col-sm-12">

            <form onSubmit={this.handleFormSubmit}>
              {this.createCheckboxes()}

            </form>

          </div>
        </div>
      </div>
    );
  }
}

export default Game;