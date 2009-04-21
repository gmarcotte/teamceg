// event contains all the code necessary to make IE and Mozilla play nice with events
var helene.event = {
	cache:[],
	get:function(evt) {
		if (!evt) {
			evt=window.event;
		}
		if (!evt.target) {
			evt.target=evt.srcElement;
		}
		return evt;
	},
	cancel:function(evt) {
		if (evt.returnValue) {
			evt.returnValue=false;
		} 
		if (evt.preventDefault) {
			evt.preventDefault();
		}
		evt.cancelBubble=true;
		if (evt.stopPropagation) {
			evt.stopPropagation();
		}
		return false;
	},
	pass:function(evt) {
		return true;
	},
	attach:function(ob, event, fp, useCapture) {
		function createHandlerFunction(obj, fn){
			// FIXME: remember handler function somewhere so we can unattach it on unload
			// perhaps remember all events per object, so you can also specifically unattach
			// events for a specific object
			var o = new Object;
			o.myObj = obj;
			o.calledFunc = fn;
			o.myFunc = function(e){ 
				var e = helene.event.get(e);
				return o.calledFunc.call(o.myObj, e);
			}
			return o.myFunc;
		}
		var handler=createHandlerFunction(ob, fp);
		helene.event.cache[helene.event.cache.length]={ event:event, object:ob, handler:handler };
		if (ob.addEventListener){
			ob.addEventListener(event, handler, useCapture);
			return true;
		} else if (ob.attachEvent){
			return ob.attachEvent("on"+event, handler);
		} else {
			//FIXME: don't do alerts like this
			alert("Handler could not be attached");
		}
	},
	clean:function() {
		var item=null;
		for (var i=helene.event.cache.length-1; i>=0; i--) {
			item=helene.event.cache[i];
			item.object['on'+item.event]=null;
			if (item.object.removeEventListener) {
				item.object.removeEventListener(item.event, item.handler, item.useCapture);
			} else if (item.object.detachEvent) {
				item.object.detachEvent("on" + item.event, item.handler);
			}
			helene.event.cache[i]=null;
		}
		item=null;
	}
}