class Friend {
	static #buttons = {
		"add": "uil-plus",
		"remove": "uil-minus"
	}

	static add = (id, classList) => {
		fetch('api/friend/add/', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'X-CSRFToken': Cookies.get('csrftoken')
			},
			body: JSON.stringify({"id": id})
		})
		   .then(response => response.json())
		   .then(response => {
			   if (response.id == id) {
				   classList.add(this.#buttons.remove);
				   classList.remove(this.#buttons.add);
			   }
		   });
	}

	static remove = (id, classList) => {
		fetch('api/friend/remove/', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'X-CSRFToken': Cookies.get('csrftoken')
			},
			body: JSON.stringify({"id": id})
		})
		   .then(response => response.json())
		   .then(response => {
			   if (response.id == id) {
				   classList.add(this.#buttons.add);
				   classList.remove(this.#buttons.remove);
			   }
		   });
	}

	static action = e => {
		var { currentTarget } = e;
		var { id, classList } = currentTarget;

		if (id) {
			if (classList.contains(this.#buttons.add)) {
				Friend.add(id, classList);
			}
			else if (classList.contains(this.#buttons.remove)) {
				Friend.remove(id, classList);
			}
		}
	}
}

(function addEvents() {
	var buttons = document.querySelectorAll(".user .uil-plus, .user .uil-minus");
	buttons.forEach((target, index, array) => {
		target.addEventListener("click", e => Friend.action(e));
	});
})()
