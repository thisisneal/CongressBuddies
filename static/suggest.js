// suggest.js - returns a list of word suggestions from an input string.
// Written by Sundeep Gottipati
// sundeep@gsundeep.com
// Initially published May 1, 2013 

// Example usage
// var words = ["koala", "koangaroo", "teddy", "teddybear"]
// var auto = new Suggester(words);

// Suggestions for input "ko"
// var matches = auto.suggest("ko");
// -> matches = ["koala", "koangaroo"]

// Suggestions for input "te"
// matches = auto.suggest("te");
// -> matches = ["teddy", "teddybear"]

// Suggestions for input "teddyb"
// matches = auto.suggest("teddyb");
// -> matches = ["teddybear"]

// Suggestions for input "xyz". No matches returns null.
// matches = auto.suggest("xyz");
// -> matches = null

// Load new list into object.
// words = ["xyzabc", koala", "koangaroo", "teddy", "teddybear"]
// auto.load(words)
// matches = auto.suggest("xyz");
// -> matches = ["xyzabc"]

function Suggester(list) {

	// process(list) - Processes list so that suggestions are returned really fast.
	this.process = function(list) {

		// copy holds a copy of the list of words.
		var copy = [];

		// Add position values to each word in list.
		for (var word_position = 0; word_position < list.length; word_position++)
			copy[word_position] = [word_position, list[word_position]];

		// position holds the position of the character we are looking for in each word.
		var position = 0;
		// temp holds the substring of the word from the first character to the character at the position value stored in the variable "position".
		var temp;

		// Keep iterating through the list until all the words have been processed and removed from copy.
		while(copy.length > 0) {
			// to_delete holds a list of words that should be removed because they have been fully processed.
			var to_delete = [];
			
			for (var current_word = 0; current_word < copy.length; current_word++) {
			
				// temp holds the substring of the word from the first character to the character at the position value stored in the variable "position".
				temp = copy[current_word][1].substring(0, position + 1);
			
				// Check if the substring already exists as a key in dict, if not add it and set its value to an empty list.
				if(this.dict[temp] === undefined)
					this.dict[temp] = [];
			
				// Push the index of the word into the list value of the substring key in dict.
				this.dict[temp].push(copy[current_word][0]);
			
				// If the substring we just dealt with is the size of the word, then we've fully processed the word. Mark the word for deletion.
				if(temp.length == copy[current_word][1].length)
					to_delete.push(current_word);
			
			}

			// Remove the words that we've marked for deletion.
			for(var word_to_delete_index = to_delete.length - 1; word_to_delete_index >= 0; word_to_delete_index--)
				copy.splice(to_delete[word_to_delete_index], 1);
			
			// Increment position so we can process words at the next character position.
			position++;
		}

	} 

	// suggest(input) - returns a set of suggestions from the provided input.
	this.suggest = function(input) {
		// If no matches, return null
		if(this.dict[input] === undefined)
			return null;

		// suggestions will hold the list of suggestions that we're returning.
		var suggestions = [];
		// Go through the list of matches and push the word associated with the index into "suggestions". 
		for (var suggestion_word_index = 0; suggestion_word_index < this.dict[input].length; suggestion_word_index++)
			suggestions.push(this.list[this.dict[input][suggestion_word_index]]);
		
		// Return the suggestions list.
		return suggestions;
	}

	// load(list) - used to load a new set of words 
	this.load = function(list) {
		// Set the object's list to the new list.
		this.list = list;
		// Empty the object's dict.
		this.dict = {};
		// Process the new list.
		this.process(this.list);
	}

	// Object data
	// list holds the list of words that we are finding suggestions from.
	this.list = list;
	// dict holds all suggestions generated from the process function.
	this.dict = {};

	// Process list on object creation
	this.process(this.list);
}