var editID = null;
var userLoggedIn = false;

var submitButton = document.querySelector('#editing-submit-button');
console.log("Submit Button: ", submitButton);

var deleteButton = document.querySelector('#editing-delete-button');
console.log("Delete Button: ", deleteButton);

var createUserSubmitButton = document.querySelector('#create-submit-button');
console.log("Create User Submit Button: ", createUserSubmitButton);

var createUserCancelButton = document.querySelector('#create-cancel-button');
console.log("Create User Cancel Button: ", createUserCancelButton);

var logInSubmitButton = document.querySelector('#login-submit-button');
console.log("Log In Submit Button: ", logInSubmitButton);

var logInCancelButton = document.querySelector('#login-cancel-button');
console.log("Log In Cancel Button: ", logInCancelButton);

var editButton = document.querySelector("#preview-edit-button");
console.log("Edit Button: ", editButton);
editButton.onclick = function() {
	if (editID == null) {
		return;
	}
	console.log("Edit Button Clicked");
	fetch('http://localhost:8080/recipes/' + editID, { credentials: 'include' }).then(function (response) {
		response.json().then(function (data) {
			var recipe = data;
			document.getElementById('blur-recipe-editing-div').style.display= 'flex';
			document.getElementById('recipe-title-editing').value= recipe.title;
			document.getElementById('recipe-date-editing').innerHTML= recipe.date;
			document.getElementById('recipe-diet-editing').value= recipe.diet;
			document.getElementById('recipe-ingredients-editing').value= recipe.ingredients;
			document.getElementById('recipe-instructions-editing').value= recipe.instructions;
			submitButton.innerHTML = 'Submit';
			deleteButton.innerHTML= 'Delete';
			submitButton.onclick = function() {
				var recipeTitle = document.getElementById('recipe-title-editing').value;
				var recipeDiet = document.getElementById('recipe-diet-editing').value;
				var recipeIngredients = document.getElementById('recipe-ingredients-editing').value;
				var recipeInstructions = document.getElementById('recipe-instructions-editing').value;
				var data = "title=" + encodeURIComponent(recipeTitle);
				data += "&diet=" + encodeURIComponent(recipeDiet);
				data += "&ingredients=" + encodeURIComponent(recipeIngredients);
				data += "&instructions=" + encodeURIComponent(recipeInstructions);
				console.log("encoded data to be sent to server:", data);
				//Send data recipe to the server
				fetch('http://localhost:8080/recipes/' + editID, {
					//headers, method, body here
					method: 'PUT',
					credentials: 'include',
					body: data,
					headers: {
						'Content-Type': 'application/x-www-form-urlencoded'
					}
				}).then(function (response) {
					//When the server responds
					//Refresh your list, repeat the get request
					loadRecipesFromServer();
					document.getElementById('blur-recipe-editing-div').style.display= 'none';
					changeDisplayDiv();
				});	
			}
			deleteButton.onclick = function() {
				if (confirm("Delete " + recipe.title +"?")) {
					deleteRecipeFromServer(editID);
					document.getElementById('blur-recipe-editing-div').style.display= 'none';
					document.getElementById('recipe-full-display-wrapper').style.display= 'none';			
					editID = null;
				}
			}
		});	
	});
};

var addButton = document.querySelector("#preview-add-button");
console.log("Add Button: ", addButton);
addButton.onclick = function() {
	console.log("Add Button Clicked");
	document.getElementById('blur-recipe-editing-div').style.display= 'flex';
	document.getElementById('recipe-title-editing').value= 'Click To Enter Title';
	document.getElementById('recipe-diet-editing').value= 'Omnivorous';
	document.getElementById('recipe-ingredients-editing').value= 'Ingredients...';
	document.getElementById('recipe-instructions-editing').value= 'Instructions...';
	submitButton.innerHTML = 'Submit';
	deleteButton.innerHTML = 'Discard';
	submitButton.onclick = function() {
		var recipeTitle = document.getElementById('recipe-title-editing').value;
		var recipeDiet = document.getElementById('recipe-diet-editing').value;
		var recipeIngredients = document.getElementById('recipe-ingredients-editing').value;
		var recipeInstructions = document.getElementById('recipe-instructions-editing').value;
		var data = "title=" + encodeURIComponent(recipeTitle);
		data += "&diet=" + encodeURIComponent(recipeDiet);
		data += "&ingredients=" + encodeURIComponent(recipeIngredients);
		data += "&instructions=" + encodeURIComponent(recipeInstructions);
		console.log("encoded data to be sent to server:", data);
		//Send data recipe to the server
		fetch('http://localhost:8080/recipes', {
			//headers, method, body here
			method: 'POST', 
			credentials: 'include',
			body: data,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			}
		}).then(function (response) {
			//When the server responds
			//Refresh your list, repeat the get request
			loadRecipesFromServer();
		});	
		document.getElementById('blur-recipe-editing-div').style.display= 'none';
	}
	deleteButton.onclick = function() {
		if (confirm("Discard " + document.getElementById('recipe-title-editing').value +"?")) {
			document.getElementById('blur-recipe-editing-div').style.display= 'none';
		}
	}
};

var addViewUserButton = document.querySelector("#profile-addview-button");
console.log("AddView Button: ", addViewUserButton);
addViewUserButton.onclick = function() {
	if (userLoggedIn == false) {
		console.log("Add/View User Button Clicked");
		document.getElementById('blur-profile-editing-div').style.display= 'flex';
		document.getElementById('profile-create-div').style.display= "block";
		document.getElementById('userExists').style.display= 'none';
		document.getElementById('allFieldsRequiredCreate').style.display= 'none';
		document.getElementById('firstName').value= '';
		document.getElementById('lastName').value= '';
		document.getElementById('emailCreateInput').value= '';
		document.getElementById('passwordCreateInput').value= '';
		createUserSubmitButton.onclick = function() {
			var firstName = document.getElementById('firstName').value;
			var lastName = document.getElementById('lastName').value;
			var email = document.getElementById('emailCreateInput').value;
			var password = document.getElementById('passwordCreateInput').value;
			if (firstName == "" || lastName == "" || email == "" || password == "") {
				document.getElementById('allFieldsRequiredCreate').style.display= 'block';
				return;
			} else {
				document.getElementById('allFieldsRequiredCreate').style.display= 'none';
			}
			var data = "firstName=" + encodeURIComponent(firstName);
			data += "&lastName=" + encodeURIComponent(lastName);
			data += "&email=" + encodeURIComponent(email);
			data += "&password=" + encodeURIComponent(password);
			console.log("encoded data to be sent to server:", data);
			//Send data recipe to the server
			fetch('http://localhost:8080/users', {
				//headers, method, body here
				method: 'POST', 
				credentials: 'include',
				body: data,
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}).then(function (response) {
				//When the server responds
				if (response.status == '422') {
					document.getElementById('userExists').style.display= 'block';
				} else {
					userLoggedIn = true;
					changeUserRelatedElements("Signed", "In");
					document.getElementById('blur-profile-editing-div').style.display= 'none';
					document.getElementById('profile-create-div').style.display= "none";
					document.getElementById('userExists').style.display= 'none';
					document.getElementById('blur-refresh-div').style.display= 'flex';
					
					loadRecipesFromServer();
				}
			});	
		}
		createUserCancelButton.onclick = function() {
			console.log("Profile Create Cancel Button Clicked");
			document.getElementById('blur-profile-editing-div').style.display= 'none';
			document.getElementById('profile-create-div').style.display= "none";
			document.getElementById('userExists').style.display= 'block';
		}
	}
};

var logInOutUserButton = document.querySelector("#profile-loginout-button");
console.log("Log In/Out Button: ", logInOutUserButton);
logInOutUserButton.onclick = function() {
	if (userLoggedIn == false) {
		console.log("Add/View User Button Clicked");
		document.getElementById('blur-profile-editing-div').style.display= 'flex';
		document.getElementById('profile-login-div').style.display= "block";
		document.getElementById('userIncorrect').style.display= 'none';
		document.getElementById('allFieldsRequiredLogin').style.display= 'none';
		document.getElementById('emailLogInInput').value= '';
		document.getElementById('passwordLogInInput').value= '';
		logInSubmitButton.onclick = function() {
			var email = document.getElementById('emailLogInInput').value;
			var password = document.getElementById('passwordLogInInput').value;
			if (email == "" || password == "") {
				document.getElementById('allFieldsRequiredLogin').style.display= 'block';
				return;
			} else {
				document.getElementById('allFieldsRequiredLogin').style.display= 'none';
			}

			var data = "email=" + encodeURIComponent(email);
			data += "&password=" + encodeURIComponent(password);
			console.log("encoded data to be sent to server:", data);
			//Send data recipe to the server
			fetch('http://localhost:8080/sessions', {
				//headers, method, body here
				method: 'POST', 
				credentials: 'include',
				body: data,
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}).then(function (response) {
				//When the server responds
				if (response.status == '401') {
					document.getElementById('userIncorrect').style.display= 'block';
				} else if (response.status == '201') {
					userLoggedIn = true;
					changeUserRelatedElements("Signed", "In");
					document.getElementById('blur-profile-editing-div').style.display= 'none';
					document.getElementById('profile-login-div').style.display= "none";
					document.getElementById('userIncorrect').style.display= 'none';
					loadRecipesFromServer();
				}
			});	
		}
		logInCancelButton.onclick = function() {
			console.log("Profile Create Cancel Button Clicked");
			document.getElementById('blur-profile-editing-div').style.display= 'none';
			document.getElementById('profile-login-div').style.display= "none";
			document.getElementById('userIncorrect').style.display= 'block';
		}
	} else {
		if (confirm("Log out?")) {
			fetch('http://localhost:8080/sessions', {
				//headers, method, body here
				method: 'DELETE', 
				credentials: 'include',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}).then(function (response) {
				//When the server responds
				if (response.status == '200') {
					userLoggedIn = false;
					changeUserRelatedElements("Anonymous", "Person");
					loadRecipesFromServer();
				} else if (response.status == '404') {
				}
			});	
		}
	}
};

function changeUserRelatedElements(firstName, lastName) {
	if (userLoggedIn == true) {
		document.getElementById('profile-name-div').innerHTML = firstName + " " + lastName;
		//addViewUserButton.innerHTML = 'View Profile';
		addViewUserButton.style.display = 'none';
		logInOutUserButton.innerHTML = 'Log Out';
	} else {
		document.getElementById('profile-name-div').innerHTML = "Anonymous Person";
		addViewUserButton.style.display = 'block';
		addViewUserButton.innerHTML = 'Sign Up';
		logInOutUserButton.innerHTML = 'Log In';
	}
};

function changeDisplayDiv() {
	fetch('http://localhost:8080/recipes/' + editID, { credentials: 'include' }).then(function (response) {
		response.json().then(function (data) {
			var recipe = data;
			document.getElementById('recipe-display-title-div').innerHTML = recipe.title;
			document.getElementById('recipe-display-date-created-div').innerHTML = recipe.date;
			document.getElementById('recipe-display-diet-div').innerHTML = recipe.diet;
			document.getElementById('recipe-display-ingredients-textarea').value = recipe.ingredients;
			document.getElementById('recipe-display-instructions-textarea').value = recipe.instructions;
			console.log("I've been changed.", recipe.title);
		});	
	});
};

function deleteRecipeFromServer(recipe_id) {
	fetch('http://localhost:8080/recipes/' + recipe_id, {
		//headers, method, body here
		method: 'DELETE', 
		credentials: 'include'
	}).then(function (response) {
		//When the server responds
		//Refresh your list, repeat the get request
		loadRecipesFromServer();
	});
};

function loadRecipesFromServer() {
	fetch("http://localhost:8080/recipes", { credentials: 'include' }).then(function (response) {
		//When the server responds:
		if (response.status == 200) {
			userLoggedIn = true;
			changeUserRelatedElements("Signed", "In");
			document.getElementById('content-hider').style.display = 'none';	
			//document.getElementById('main-content-wrapper').style.display = 'block';	
		} else if (response.status == 401) {
			document.getElementById('content-hider').style.display = 'block';	
			//document.getElementById('main-content-wrapper').style.display = 'none';	
			return;
		}
		//display the list of resource records
		response.json().then(function (data) {
			//data is now available
			//save data from server into recipes variable
			//so that we can use the data in our app.
			recipes = data;
			//for (var i = 0; i < ?; i++)
			//query the parent element
			var previewDiv = document.querySelector("#previewListDiv");
			//CLEAR THE LIST SO THAT WE DON'T DUPLICATE
			previewDiv.innerHTML = ""
			recipes.forEach(function (recipe) {
				//Insert a new element into the document
				//1: create a new element and give whatever is in text box.
				var newRecipePreviewDiv = document.createElement("div");
				newRecipePreviewDiv.className="recipe-preview-content-wrapper";
				previewDiv.appendChild(newRecipePreviewDiv);

				var titleDiv = document.createElement("div");
				titleDiv.innerHTML = recipe.title;
				titleDiv.className="recipe-preview-title";
				newRecipePreviewDiv.appendChild(titleDiv);

				var dateDiv = document.createElement("div");
				dateDiv.innerHTML = recipe.date;
				dateDiv.className="recipe-preview-date";
				newRecipePreviewDiv.appendChild(dateDiv);

				var dietDiv = document.createElement("div");
				dietDiv.innerHTML = recipe.diet;
				dietDiv.className="recipe-preview-diet";
				newRecipePreviewDiv.appendChild(dietDiv);

				//This is to display recipe to commoners
				newRecipePreviewDiv.onclick = function () {
					console.log("Recipe ID: ", recipe.id);
					//1. Remember the record ID
					editID = recipe.id;
					console.log("Edit ID: ", editID);
					//2. Show any inputs and/or buttons for editing
					document.getElementById('recipe-full-display-wrapper').style.display= 'block';			
					//3. Assign input values to the fields for editing
					changeDisplayDiv();
				};
			});
		});
	});
};


loadRecipesFromServer();


























	//var randomNumber = Math.floor(Math.random() * lunchPlaces.length);
	//var randomLunchPlace = lunchPlaces[randomNumber];
	
	//Changing Header to Match Place Found
	//heading.innerHTML = randomLunchPlace;
	//heading.style.color = "#FFCC00";
