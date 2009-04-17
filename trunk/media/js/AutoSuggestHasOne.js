function remove_assignone_id(object_name, id) {
	// Show input
	input = $('id_' + object_name + '_input');
	input.setStyle('display', 'inline');
	
	// Clear value
	hidden_input = $('id_' + object_name);
	hidden_input.value = "";
	
	// Remove object name
	display_el = $(object_name + '_' + id);
	
	if (display_el != false) {
		display_el.remove();
	}
}

function autosuggesthasone_options(url, object_name) {
	return {
		script:url,
		varname:"q",
		json:true,
		shownoresults:true,
		maxresults:6,
		callback: function (obj) {
			// Update value
			hidden_input = $('id_' + object_name);
			hidden_input.value = obj.id;
			
			// Hide input
			input = $('id_' + object_name + '_input');
			input.setStyle('display', 'none');
			
			// Display object name
			new_el = new Element('span', 
								{'id': object_name + '_' + obj.id, 
								 'styles': {'color': 'green'}});
			new_el.setHTML(obj.value + ' <a href="#" onclick="remove_assignone_id(\'' + object_name + '\',\'' + obj.id + '\'); return false;">[Remove]</a>');
			new_el.injectBefore($('id_' + object_name));	
		}	
	}
}

window.addEvent('domready', function() {
	$$('input.vModelHasOneWidget').each(function(el_input){
		object_name = el_input.getProperty('name');
		object_name = object_name.substring(0, object_name.lastIndexOf('_input'));
		url = el_input.getProperty('src');
		
		new bsn.AutoSuggest('id_' + object_name + '_input', autosuggesthasone_options(url, object_name));
	});
});