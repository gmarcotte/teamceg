// position is a utility object to return line, column and character position
helene.position = function(line, column, character) {
	this.line		= line;
	this.column		= column;
	this.character	= character;
	this.compare	= function(pos) {
		if (this.line < pos.line) {
			return -1;
		} else if (this.line > pos.line) {
			return 1;
		} else if (this.column < pos.column) {
			return -1;
		} else if (this.column > pos.column) {
			return 1;
		} else {
			return 0;
		}
	}
	this.largerThan	= function(pos) {
		return this.compare(pos)==1;
	}
	this.smallerThan = function(pos) {
		return this.compare(pos)==-1;
	}
}