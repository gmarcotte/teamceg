// line is a LI item, with additions, each of which contains one line of the source
helene.line = function() {
	this.className	='hlLine';
	var length		= 0;
	var source		= new String('');

	this.init = function(editor) {
		this.editor = editor;
		helene.event.attach(this, 'mousedown', helene.mouse.onMouseDown);
		helene.event.attach(this, 'mouseup', helene.mouse.onMouseUp);
	}

	this.setContent = function(sourceLine) {
		source = sourceLine.replace(new RegExp('\n','gim'), '').replace(new RegExp('\r','gim'), '');
		var processedLine = helene.util.tabs.replace(source);
		processedLine = processedLine.replace(/ /g, "\u00A0");
		length = processedLine.length;
		var text = document.createTextNode(processedLine +"\u00A0"); // add a space to make firefox display the correct line height
		if (this.firstChild) {
			this.replaceChild(text, this.firstChild);
		} else {
			this.appendChild(text);
		}
	}

	this.getContent = function() {
		return source;
	}

	this.getLength = function() {
		return length;
	}
}
