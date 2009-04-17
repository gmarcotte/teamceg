// util contains a few usefull methods to work with dom stuff, tabs, etc.
helene.util = {
	applyInherit:function(orig, interf) {
		for (method in interf) {
			orig[method] = interf[method];
		}
		return orig;
	},

	createElement:function(tagName) {
		switch(tagName) {
			case 'editorCanvas':
				return helene.util.applyInherit(document.createElement("DIV"), new helene.canvas());
			break;
			case 'editorInput':
				return helene.util.applyInherit(document.createElement("TEXTAREA"), new helene.input());
			break;
			case 'editorDocument':
				return helene.util.applyInherit(document.createElement("OL"), new helene.content());
			break;
			case 'editorLine':
				return helene.util.applyInherit(document.createElement("LI"), new helene.line());
			break;
			default:
				return document.createElement(tagName);
		}
	},

	createStyleSheet:function(href) {
		if(document.createStyleSheet) {
			document.createStyleSheet(href);
		} else {
			var newSS	= document.createElement('link');
			newSS.rel	= 'stylesheet';
			newSS.type	= 'text/css';
			newSS.href	= href;
			document.getElementsByTagName("head")[0].appendChild(newSS);
		}
	},

	tabs:{
		
		replace:function(line) {
			// Note that the tabbing code here is now obsolete because we have replaced
      // tabs with spaces -- NOTE THAT THIS MEANS THE USER CANNOT put an actual tab
      // character in their stuff... CCI ???
			var tempTab			= "\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0";
			var tempLine		= line;
			var tempIndex		= -1;
			var counter			= 0;
			var spaceCount		= 0;
			var processedLine	= '';
			do {
				tempIndex = tempLine.indexOf("\t");
				if (tempIndex != -1) {
					processedLine += tempLine.substr(0, tempIndex);
					counter += tempIndex;
					spaceCount = helene.options.tabSize-(counter%helene.options.tabSize);
					processedLine += tempTab.substr(0, spaceCount);
					counter += spaceCount;
					tempLine = tempLine.substr(tempIndex+1, tempLine.length);
				} else {
					processedLine += tempLine;
				}
			} while (tempIndex != -1);
			return processedLine;
		},
		
		columnToCharPos:function(column, line) {
			var colCounter	= 0;
			var charCounter	= 0;
			var tempLine	= new String(line);
			var nextChar;
			var realTabSize;
			do {
				nextChar = tempLine.charAt(charCounter);
				// walk through the string a character at a time
				// FIXME: this can be sped up
				charCounter++;
				if (nextChar == '\t') {
					realTabSize = helene.options.tabSize-(colCounter%helene.options.tabSize);
					colCounter += realTabSize;
				} else {
					colCounter++;
				}
			} while (nextChar && colCounter<column);
			return charCounter;
		},
		
		charPosToColumn:function(charPos, line) {
			var colCounter	= 1;
			var charCounter	= 0;
			var tempLine	= line;
			var nextChar;
			var realTabSize;
			while (charCounter < (charPos-1)) {
				// walk through the string a character at a time
				// FIXME: this can be sped up
				nextChar = tempLine.charAt(charCounter);
				charCounter++;
				if (nextChar == '\t') {
					realTabSize = helene.options.tabSize-((colCounter-1)%helene.options.tabSize);
					colCounter += realTabSize;
				} else {
					colCounter++;
				}
				if (!nextChar) {
					break;
				}
			}
			return colCounter;		
		},
		
		getRealColumn:function(column, line, skipTabs) {
			// returns the column the cursor should be put on
			// taking into account the cursor cannot be put in a tab
			// if skipTabs is true, the cursor will be put to the right
			// of the tab, if the cursor would otherwise be anywhere in
			// the tab. Otherwise, the cursor is put to the left.
			var colCounter	= 1;
			var charCounter	= 0;
			var tempLine	= line;
			var nextChar;
			var realTabSize;
			while (colCounter < column) {
				// walk through the string a character at a time
				// FIXME: this can be sped up
				nextChar = tempLine.charAt(charCounter);
				charCounter++;
				if (nextChar == '\t') {
					realTabSize = helene.options.tabSize-((colCounter-1)%helene.options.tabSize);
					colCounter += realTabSize;
				} else {
					colCounter++;
				}
				if (!nextChar) {
					break;
				}
			}
			if (!skipTabs && nextChar == '\t' && colCounter > column) {
				// if the last character was a tab, and the column is left of the colCounter column,
				// set the cursor to the left of the tab.
				colCounter -= realTabSize;
			}
			return colCounter;
		}
	}
}

