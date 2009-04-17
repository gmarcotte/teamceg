// canvas contains all visible elements of the editor
helene.canvas = function() {
	this.className = 'hlCanvas';
	this.init = function(editor) {
		this.editor = editor;

		// try to read font sizes and font style from the textarea
		if (this.editor.source.currentStyle) {
			var style = this.editor.source.currentStyle;
		} else {
			var style = document.defaultView.getComputedStyle(this.editor.source, "");
		}
		if (style) {
			if (this.style.setProperty) {
				for (var i=0; i<style.length; i++) {
					this.style.setProperty(style.item(i), style.getPropertyValue(style.item(i)), "");
				}
			} else {
				for (var i in style) {
					this.style[i] = style[i];
				}
			}
			this.style.fontFamily = style.fontFamily;
			this.style.fontSize = style.fontSize;
			this.style.color = style.color;

		}
		// position the canvas so it overlaps the textarea exactly
		this.canvasWidth = this.editor.source.offsetWidth;
		this.canvasHeight = this.editor.source.offsetHeight;
		this.style.width = this.canvasWidth+'px';
		this.style.height = this.canvasHeight+'px';

		// add the input line
		this.input = helene.util.createElement('editorInput'); //new helene.input(this);
		this.input.init(editor);
		this.appendChild(this.input);

		// add the content area
		this.content = helene.util.createElement('editorDocument'); //new helene.document(this);
		this.content.init(editor);
		this.appendChild(this.content);

		// calculate letterWidth
		this.letterWidth = this.content.getLetterWidth();

		// get border width to calculate inner width of canvas
		var temp = new String(this.style.borderLeftWidth);
		this.borderWidth = new Number(temp.replace(/px/,''));
		temp = new String(this.style.borderRightWidth);
		this.borderWidth = this.borderWidth+new Number(temp.replace(/px/,''));
		this.scrollLeft = '0px';
		
		helene.event.attach(this, 'mousedown', helene.mouse.onMouseDown);
		helene.event.attach(this, 'mouseup', helene.mouse.onMouseUp);
	}
}